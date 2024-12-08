import psycopg2
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

pg_config = {
    'dbname': 'hh_vacancies',
    'user': 'postgres',
    'password': '12345678',
    'host': 'localhost',
    'port': '5433',
}

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def update_sheet():
    conn = psycopg2.connect(**pg_config)
    query = "SELECT * FROM vacancies"
    data = pd.read_sql_query(query, conn)

    df = pd.DataFrame(data)

    df.drop('id', axis=1, inplace=True)
    df = df.fillna('')
    for column in df.select_dtypes(include=[np.datetime64, 'datetime']):
        df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')

    creds = ServiceAccountCredentials.from_json_keyfile_name("hhvacancy-1c1f9533d937.json", scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open("hh_vacancies")
    worksheet = spreadsheet.sheet1

    start_row = 1
    end_row = len(df) + 1

    range_of_cells = f"A{start_row}:M{end_row}"

    worksheet.update([df.columns.values.tolist()] + df.values.tolist(), range_of_cells)
    print(f'{end_row} строк обновлено')

update_sheet()

