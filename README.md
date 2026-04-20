# Fact-Check Agent (Automated Claim Verification System)

## Overview

The Fact-Check Agent is a web-based application that automatically verifies factual claims from uploaded PDF documents. It acts as a “truth layer” by extracting statements, cross-checking them against live web data, and classifying them as **Verified**, **Inaccurate**, or **False**.

This project is designed to address the growing issue of misinformation, outdated statistics, and hallucinated content in marketing and informational documents.

---

## Features

* PDF Upload Interface (Streamlit)
* Automatic Text Extraction from PDF
* Claim Detection using NLP heuristics
* Real-time Fact Verification using:

  * Wikipedia (primary source)
  * DuckDuckGo search (fallback)
* AI-based Reasoning using Mistral API
* Classification Output:

  * Verified
  * Inaccurate
  * False
* Confidence Score for each claim
* Evidence Snippet Display
* Clean and color-coded UI for readability

---

## System Architecture

1. Input Layer
   User uploads a PDF document.

2. Extraction Layer
   Text is extracted using PyMuPDF.

3. Claim Detection
   Sentences containing factual indicators (numbers, assertions, keywords) are identified as claims.

4. Retrieval Layer

   * Wikipedia API is used to fetch reliable summaries
   * DuckDuckGo is used as a fallback search mechanism

5. Reasoning Layer
   Mistral LLM processes the claim and evidence to determine factual correctness.

6. Output Layer
   Claims are classified and displayed with explanation, confidence score, and supporting evidence.

---

## Tech Stack

* Frontend: Streamlit
* Backend: Python
* PDF Processing: PyMuPDF
* Web Scraping: BeautifulSoup, Requests
* LLM: Mistral API
* Deployment: Streamlit Community Cloud

---

## Installation (Local Setup)

1. Clone the repository

```bash
git clone https://github.com/AshrafEqbal/Fact-Checker
cd [Fact-Checker
```

2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate 
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add environment variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_api_key_here
```

5. Run the application

```bash
streamlit run app.py
```

---

## Deployment

This project is deployed using Streamlit Community Cloud.

Steps:

* Push code to GitHub repository
* Connect repository to Streamlit Cloud
* Set `app.py` as entry point
* Add API key in Streamlit Secrets:

```toml
MISTRAL_API_KEY = "your_api_key_here"
```

---

## Usage

1. Open the deployed application
2. Upload a PDF file containing textual claims
3. Wait for processing
4. View:

   * Extracted claims
   * Classification (Verified / Inaccurate / False)
   * Explanation
   * Confidence score
   * Supporting evidence

---

## Example Claims Tested

* “India’s population reached 1.2 billion in 2011” → Verified
* “COVID-19 began in 2018” → False
* “90% of world data created in last 2 years” → Inaccurate
* “Human body has 206 bones” → Verified

---

## Limitations

* Depends on availability and accuracy of web data
* Wikipedia summaries may not cover all claims
* Complex or ambiguous claims may reduce accuracy
* Rate limits may apply for API usage

---

## Future Improvements

* Multi-source verification (news APIs, research databases)
* Highlight incorrect numerical values in claims
* Export report as PDF
* Improve claim detection using advanced NLP models
* Add citation links for verified evidence

---

## Conclusion

This project demonstrates a practical implementation of a retrieval-augmented fact-checking system combining web data and LLM reasoning. It provides a scalable approach to improving content reliability and detecting misinformation.

---

## Author

Ashraf Eqbal
B.Tech AI & ML
Amity University Gurugram
