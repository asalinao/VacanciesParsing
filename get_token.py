import requests

url = "https://hh.ru/oauth/token"

# Параметры для тела запроса
payload = {
    "grant_type": "authorization_code",
    "client_id": "JB4CAPJBKN7ATJVVEFETO2L2BAKOT8G7N9TE5T02DD2ONEGKJICFK76V7TIBQKU7",         # Замените на ваш client_id
    "client_secret": "HB28T6RQIRRKPMTGUDC75BRTOROIITPP4UAUTHE4HCR34VSC048D4R303JKBUHGJ", # Замените на ваш client_secret
    "code": "QFRVNFH0C31V0L9G7H4E0PKSCTRF87BJMVJFQ6DU5PQNI1A79TCNV9N39F2MV9Q1",                   # Замените на код авторизации
    "redirect_uri": "https://example.com/page"    # Замените на ваш redirect_uri
}

# Заголовки
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Выполнение запроса
response = requests.post(url, data=payload, headers=headers)

# Обработка ответа
if response.status_code == 200:
    print("Access Token:", response.json().get("access_token"))
else:
    print("Error:", response.status_code, response.text)