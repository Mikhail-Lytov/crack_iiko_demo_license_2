import requests
import json
import hashlib

URL_IIKO_BACKEND = ''
USER_LOGIN = ""
USER_PASSWORD = ""


def sha1_hash(string):
  """Вычисляет SHA-1 хеш строки."""
  sha1 = hashlib.sha1()
  sha1.update(string.encode('utf-8'))
  return sha1.hexdigest()

def get_auth():
    """Получить токен авторизации"""
    url = URL_IIKO_BACKEND + "/resto/api/auth"
    print(url)
    params = {
        "login": USER_LOGIN,
        "pass": sha1_hash(USER_PASSWORD),
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.content.decode('utf-8')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None

def log_out(token):
    """Отвязать токен авторизации"""
    url = URL_IIKO_BACKEND + "/resto/api/logout"

    headers = {}
    headers["Cookie"] = 'key=' + token

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None

def get_document_by_filet(date_from, date_to, token, status=None, revision_from=-1):
    """
    Отправляет GET-запрос для получения списка приказов и выводит результат.
    """
    url = URL_IIKO_BACKEND + "/resto/api/v2/documents/menuChange"

    params = {
        "dateFrom": date_from,
        "dateTo": date_to,
    }
    headers = {}
    headers["Cookie"] = 'key=' + token

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        print("Успешно получены данные:")
        print(json.dumps(data, indent=2))

        return data

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        print(f"Ответ сервера: {response.text}") #вывод сырого ответа для отладки
        return None

def create_new_document(token, dateIncoming, dateTo, productId, price):
    """Создание нового приказа в backOffice"""
    url = URL_IIKO_BACKEND + "/resto/api/v2/documents/menuChange"
    menu_data = {
        "dateIncoming": dateIncoming,
        "status": "NEW",
        "shortName": "",
        "deletePreviousMenu": False,
        "dateTo": dateTo,
        "items": [
            {
                "num": 0,
                "departmentId": "127b40f0-25ae-bf8e-018c-8b4efa610011",
                "productId": productId,
                "productSizeId": None,
                "including": True,
                "price": price,
                "pricesForCategories": [],
                "includeForCategories": [],
                "flyerProgram": False,
                "dishOfDay": False
            }
        ]
    }

    headers = {}
    headers["Cookie"] = 'key=' + token
    headers["Content-Type"] = "application/json"

    try:
        response = requests.post(url, headers=headers, data=json.dumps(menu_data))
        response.raise_for_status()
        print("JSON успешно отправлен. Код ответа:", response.status_code)
        print("Ответ сервера:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке JSON: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON ответа: {e}")

def get_all_items(token):
    """Получить все объекты из backOffice"""
    url = URL_IIKO_BACKEND + "/resto/api/v2/entities/products/list?includeDeleted=false"
    headers = {"Cookie": 'key=' + token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        print(f"Ответ сервера: {response.text}")
        return None