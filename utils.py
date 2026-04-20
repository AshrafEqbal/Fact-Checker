import fitz
import re
import requests
import urllib.parse
from bs4 import BeautifulSoup
import os
import json
import streamlit as st

# PDF TEXT
def extract_text_from_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text() + "\n"
    return text


# IMPROVED CLAIM EXTRACTION
def extract_claims(text):
    text = text.replace("\n", " ")
    sentences = re.split(r'(?<=[.!?]) +', text)
    claims = []
    for s in sentences:
        s = s.strip()
        if len(s) < 20:
            continue
        if re.search(r'\d', s) or any(word in s.lower() for word in [
            "is", "are", "was", "were", "has", "have", "according", "study"
        ]):
            claims.append(s)
    return list(dict.fromkeys(claims))  # remove duplicates


#  CLEAN QUERY 
def clean_query(claim):
    claim = re.sub(r'[^a-zA-Z0-9 ]', '', claim)
    return " ".join(claim.split()[:6])


#  WIKIPEDIA 
def search_wikipedia(query):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("extract", "")
    except:
        pass
    return ""


#  DUCKDUCKGO 
def search_duckduckgo(query):
    query = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for r in soup.find_all("div", class_="result__body"):
            snippet = r.find("a", class_="result__snippet")
            if snippet:
                results.append(snippet.get_text())
        return " ".join(results[:5])
    except:
        return ""


#  EVIDENCE 
def get_evidence(claim):
    query = clean_query(claim)
    wiki = search_wikipedia(query)
    if wiki:
        return wiki
    return search_duckduckgo(query)


#  MISTRAL 
def call_mistral(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['MISTRAL_API_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    res = requests.post(url, headers=headers, json=data)
    if res.status_code != 200:
        return res.text
    return res.json()["choices"][0]["message"]["content"]


#  VERIFY 
def verify_claim(claim):
    evidence = get_evidence(claim)

    prompt = f"""
    Fact-check this claim.

    Claim:
    {claim}

    Evidence:
    {evidence}

    Classify:
    - Verified
    - Inaccurate
    - False

    Give:
    - short explanation (max 2 lines)
    - confidence (0-100%)

    Output JSON:
    {{
        "status": "",
        "explanation": "",
        "confidence": ""
    }}
    """

    try:
        output = call_mistral(prompt)
        match = re.search(r'\{.*\}', output, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            result = {
                "status": "Unknown",
                "explanation": output,
                "confidence": "50%"
            }
        result["evidence"] = evidence[:300]
        return result

    except Exception as e:
        return {
            "status": "Error",
            "explanation": str(e),
            "confidence": "0%",
            "evidence": ""
        }
