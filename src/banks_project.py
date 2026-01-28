import pandas as pd
import numpy as np
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3


def log_progress(message):
    timestamp_format = '%Y-%b-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("code_log.txt", "a") as f:
        f.write(f"{timestamp} : {message}\n")


def extract(url):
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    df = pd.DataFrame(columns=["Rank", "Bank name", "MC_USD_Billion"])

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            rank = cols[0].text.strip()
            bank_name = cols[1].text.strip()

            try:
                mc_val = cols[2].text.strip()
                mc_float = float(mc_val[:-1])
            except:
                continue
            data_dict = {
                "Rank": rank,
                "Bank name": bank_name,
                "MC_USD_Billion": mc_float,
            }

            df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
    return df


def transform(df, csv_path):
    exchange_rates = pd.read_csv(csv_path)
    rates = exchange_rates.set_index('Currency').to_dict()['Rate']

    df['MC_GBP_Billion'] = [np.round(x * rates['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * rates['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * rates['INR'], 2) for x in df['MC_USD_Billion']]

    return df


def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)


def load_to_db(df, sql_connection_path, table_name):
    conn = sqlite3.connect(sql_connection_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()


def run_query(query_statement, sql_connection_path):
    conn = sqlite3.connect(sql_connection_path)
    query_result = pd.read_sql(query_statement, conn)
    print(query_result)
    conn.close()


# --- Execution ---

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
exchange_rate_path = '../data/exchange_rate.csv'
table_name = 'Largest_banks'
db_path = '../data/Banks.db'
output_csv = '../data/Largest_banks_data.csv'
log_progress("Extraction start")
df = extract(url)

log_progress("Extraction complete, transformation start")
df = transform(df, exchange_rate_path)

log_progress("Transformation complete, loading start")
load_to_csv(df, output_csv)
load_to_db(df, db_path, table_name)

log_progress("Loading complete, running query")
query_statement = f"SELECT * FROM {table_name} WHERE MC_USD_Billion > 100"
run_query(query_statement, db_path)
query_statement = f"SELECT AVG(MC_GBP_Billion) FROM {table_name}"
run_query(query_statement, db_path)
query_statement = f"SELECT [Bank name] FROM {table_name} LIMIT 5"
run_query(query_statement, db_path)
log_progress("Process complete")