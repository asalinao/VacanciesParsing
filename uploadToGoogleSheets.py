import clickhouse_connect
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
def upload_vacancies():
    client = clickhouse_connect.get_client(host='localhost', username='default', password='a', port='8123')

    query = "SELECT * FROM vacancies"
    df = client.query_df(query)
    client.close()

    df = df.fillna('')
    print(df.info())
    df['published_at'] = df['published_at'].dt.strftime('%Y-%m-%d %H:%M:%S')

    creds = ServiceAccountCredentials.from_json_keyfile_name("hhvacancy-04d0d07b0d5b.json", scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open("hh_vacancies")
    worksheet = spreadsheet.sheet1

    start_row = 1
    end_row = len(df) + 1

    range_of_cells = f"A{start_row}:M{end_row}"

    worksheet.update([df.columns.values.tolist()] + df.values.tolist(), range_of_cells)




