import requests
from datetime import datetime
import clickhouse_connect
from constants import ACCESS_TOKEN
import re

QUERIES = [
    'Бизнес аналитик',
    'Аналитик данных',
    'Продуктовый аналитик',
    'Аналитик BI',
    'Младший аналитик'
    'NLP инженер',
    'Data scientist',
    'ML-инженер',
    'Инженер данных',
    'ML Researcher',
    'Deep Learning engineer',
]

COLUMNS = [
    "vacancy_id",
    "field",
    "name",
    "has_test",
    "address_city",
    "alternate_url",
    "salary_from",
    "salary_to",
    "salary_currency",
    "published_at",
    "employer_name",
    "schedule",
    "pos_level"
]

def get_vacancies():
    client = clickhouse_connect.get_client(host='localhost', username='default', password='a', port='8123')

    for query_string in QUERIES:
        url = 'https://api.hh.ru/vacancies'
        par = {'text': query_string, 'per_page': '10', 'page': 0, 'search_field': 'name'}
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
        r = requests.get(url, params=par, headers=headers).json()
        pages = r['pages']
        found = r['found']

        vacancies_from_response = []

        for i in range(0, pages + 1):
            par = {'text': query_string, 'per_page': '10', 'page': i, 'search_field': 'name'}
            r = requests.get(url, params=par, headers=headers).json()
            try:
                vacancies_from_response.append(r['items'])
            except Exception as E:
                continue

        for item in vacancies_from_response:
            for vacancy in item:
                vacancy_id = vacancy['id']
                if client.command(f"SELECT EXISTS(SELECT 1 FROM vacancies WHERE vacancy_id = {vacancy_id})") > 0:
                    continue
                name = vacancy['name'].replace("'", "").replace('"', '')
                has_test = int(vacancy['has_test'])

                try:
                    address_city = vacancy['address']['city']
                except TypeError:
                    address_city = None
                alternate_url = vacancy['alternate_url']

                try:
                    salary_from = vacancy['salary']['from']
                except TypeError as E:
                    salary_from = None

                try:
                    salary_to = vacancy['salary']['to']
                except TypeError as E:
                    salary_to = None

                try:
                    salary_currency = vacancy['salary']['currency']

                    salary_currency = salary_currency.replace('RUR', 'RUB')
                    salary_currency = salary_currency.replace('BYR', 'BYN')

                except TypeError as E:
                    salary_currency = None

                published_at = vacancy['published_at']
                published_at = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%S%z')

                employer_name = vacancy['employer']['name'].replace("'", "").replace('"', '')

                try:
                    schedule = vacancy['schedule']['id']
                except Exception as E:
                    print(E)
                    schedule = ''

                if schedule == 'flyInFlyOut':
                    continue

                field = query_string.replace('"', '')

                if re.search(r'junior|Jr|jun|младший', name.lower()):
                    pos_level = 'Junior'
                elif re.search(r'middle|mid|мид', name.lower()):
                    pos_level = 'Middle'
                elif re.search(r'senior|sr|сеньор|старший', name.lower()):
                    pos_level = 'Senior'
                elif re.search(r'стажер|стажировка', name.lower()):
                    pos_level = 'Intern'
                else:
                    pos_level = None

                new_vacancy = [[
                    vacancy_id,
                    field,
                    name,
                    has_test,
                    address_city,
                    alternate_url,
                    salary_from,
                    salary_to,
                    salary_currency,
                    published_at,
                    employer_name,
                    schedule,
                    pos_level
                ]]

                client.insert('vacancies', new_vacancy, column_names=COLUMNS)
    client.close()

get_vacancies()