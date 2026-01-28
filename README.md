# ⚙️ FinData Currency Engine (ETL)

A high-performance **ETL Pipeline** built to extract global financial market capitalization data, perform real-time currency conversions, and store structured results for financial analysis.

---

## 🚀 Overview
The **FinData Currency Engine** automates the entire data lifecycle:
1.  **Extraction**: Pulls raw financial data from web sources using `BeautifulSoup`.
2.  **Transformation**: Converts USD market caps into **GBP**, **EUR**, and **INR** using dynamic exchange rates.
3.  **Loading**: Saves the processed data into an **SQLite3** database and a structured **CSV** file.



---

## 🛠️ Tech Stack
* **Language**: Python 3.11
* **Data Processing**: Pandas
* **Web Scraping**: BeautifulSoup4 & Requests
* **Database**: SQLite3
* **Logging**: Python Logging Module

---

## 📁 Project Structure
```text
FinData-Currency-Engine/
├── data/
│   ├── exchange_rate.csv       # Reference currency data
│   ├── Financial_Data.db       # Final SQLite database
│   └── final_report.csv        # Processed CSV output
├── logs/
│   └── engine_log.txt          # Detailed process tracking
├── src/
│   └── currency_engine.py      # Main ETL logic
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
🔄 The Engine Workflow
1. Extraction 📥
The engine targets financial tables to extract Entity Name and Market Cap (USD). It handles HTML parsing and cleans up any unwanted tags or references.

2. Transformation Logic ⚙️
This is where the "Engine" does the heavy lifting:

Currency Scaling: Multiplies the USD value by exchange rates fetched from the API/CSV.

Precision: All financial metrics are rounded to 2 decimal places.

Cleaning: Removes symbols ($, £, €) to ensure pure numerical data for analysis.

3. Loading 💾
The cleaned data is loaded into the Market_Cap table in the SQLite database. This allows for high-speed SQL queries and reporting.