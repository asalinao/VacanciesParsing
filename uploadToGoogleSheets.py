import clickhouse_connect
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def upload_vacancies():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/root/hh_vacancies/hhvacancy-04d0d07b0d5b.json", scope)
    gspread_client = gspread.authorize(creds)
    spreadsheet = gspread_client.open("hh_vacancies")
    worksheet = spreadsheet.sheet1

    clickhouse_client = clickhouse_connect.get_client(host='localhost', username='default', password='a', port='8123')
    batch_size = 1000
    offset = 0
    columns = None
    total_rows = 0

    while True:
        query = f"SELECT * FROM vacancies LIMIT {batch_size} OFFSET {offset}"
        df = clickhouse_client.query_df(query)

        if df.empty:
            break

        df = df.fillna('')
        df['published_at'] = df['published_at'].dt.strftime('%Y-%m-%d %H:%M:%S')

        if columns is None:
            columns = df.columns.values.tolist()
            worksheet.update([columns], "A1")

        start_row = offset + 2
        end_row = start_row + len(df)
        range_of_cells = f"A{start_row}:M{end_row}"

        worksheet.update(df.values.tolist(), range_of_cells)
        offset += batch_size
        total_rows += len(df)
        print(f'{len(df)} строк обновлено')

        clickhouse_client.close()
    print(f'Всего обновлено {total_rows} строк')
