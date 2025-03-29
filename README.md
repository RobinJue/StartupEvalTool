# 🚀 Automated Startup Evaluation using Financial Modeling and AI

This repository contains the implementation of a proof-of-concept system designed to automate the evaluation of early-stage startups using publicly available information and AI-powered data extraction. The project was developed as part of a Bachelor's thesis at Kiel University.

It integrates a simplified Venture Capital valuation model with a Python-based data collection and processing pipeline, capable of scraping online information, extracting structured financial data using LLMs, and outputting results in a Google Sheets dashboard.

## 📌 Project Summary

The goal is to assess whether financial models and AI technologies can automate startup evaluation by:
- 📊 Forecasting and estimating startup value based on public sources
- 📈 Integrating macroeconomic indicators into valuation logic
- 🤖 Leveraging generative AI to extract data from unstructured web content

The core output is a financial snapshot that mimics investor reasoning, built entirely from non-proprietary sources.

## 🧠 Technologies Used

<details>
<summary>Click to expand technology stack</summary>

| Category | Technology / Library |
|----------|---------------------|
| **🐍 Programming Language** | Python 3.13.2 |
| **🌐 Web Framework** | Flask (for GUI and API access) |
| **💹 Financial Data Modeling** | `pandas`, `datetime`, `json` |
| **🕷️ Web Scraping** | `requests`, `BeautifulSoup`, Google Custom Search API |
| **🤖 AI & NLP Integration** | OpenAI GPT-4 via `openai` SDK |
| **📊 Google API Integration** | `googleapiclient`, `google-auth` |
| **📑 Spreadsheet Automation** | Google Sheets API, Apps Script |
| **🔧 Environment Management** | `dotenv` |
| **📝 Logging & Debugging** | Python `logging` |
| **⚙️ Process Control** | `subprocess`, `os`, `sys` |
| **📊 Visualization** | `graphviz`, BPMN diagrams |
| **🔑 Token Management** | `pickle` |

</details>

## 📁 Project Structure

```bash
project/
├── access_point/     # API and GUI (Flask + HTML)
├── config/          # Credentials and environment setup
├── gsheets/         # Google Sheets integration
├── modules/         # Core functionality
├── table/          # Financial modeling logic
├── utils/          # Helper functions
├── main.py         # Pipeline orchestrator
└── docs/           # Documentation assets
```

## 📜 License

<details>
<summary>Creative Commons Attribution-NonCommercial 4.0</summary>

This project is licensed under CC BY-NC 4.0

You are free to:
* 📋 Share — copy and redistribute the material
* 🔄 Adapt — remix, transform, and build upon the material

Under these terms:
* 🚫 NonCommercial use only
* ℹ️ Attribution required

[Full License Details](https://creativecommons.org/licenses/by-nc/4.0/)
</details>

## 📚 Academic Reference

**Author:** Robin Jüngerich  
**Institution:** Faculty of Technology, Kiel University  
**Year:** 2025

**Thesis Title:**  
"To what extent can financial models and AI technologies enable the automated evaluation of startups using publicly available information, and what are the resource requirements for its development?"

**Supervision:**
* First Supervisor: Prof. Dr. Andreas Speck
* Second Referee: Dr.-Ing. Melanie Windrich

## 📬 Contact

For academic or non-commercial inquiries:

**Robin Jüngerich**
* 📧 Academic: stu237129@mail.uni-kiel.de
* 📧 Personal: robin.juengerich@icloud.com