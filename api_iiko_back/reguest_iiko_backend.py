import requests
import json
import hashlib
import logging

URL_IIKO_BACKEND = ''
USER_LOGIN = ""
USER_PASSWORD = ""

logger = logging.getLogger()

def log():
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('crack_iikoRMS_demo_license.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

def sha1_hash(string):
  """Вычисляет SHA-1 хеш строки."""
  sha1 = hashlib.sha1()
  sha1.update(string.encode('utf-8'))
  return sha1.hexdigest()

def get_auth():
    """Получить токен авторизации"""
    url = URL_IIKO_BACKEND + "/resto/api/auth"
    logger.info(url)
    params = {
        "login": USER_LOGIN,
        "pass": sha1_hash(USER_PASSWORD),
    }

    try:
        logger.info("Request: GET " + "\nparams: " + str(params))
        response = requests.get(url, params=params)
        logger.info("Response: " + str(response))
        response.raise_for_status()

        return response.content.decode('utf-8')
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при отправке запроса: " + str(e.msg))
        return None

def log_out(token):
    """Отвязать токен авторизации"""
    url = URL_IIKO_BACKEND + "/resto/api/logout"

    headers = {}
    headers["Cookie"] = 'key=' + token

    try:
        logger.error("Request: GET " + "\nparams: " + "\nheaders: " + str(headers))
        response = requests.get(url, headers=headers)
        logger.error("Response: " + str(response))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при отправке запроса: " + str(e.msg))
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

        logger.info("Успешно получены данные:")
        logger.info(str(json.dumps(data, indent=2)))

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при отправке запроса: " + str(e.msg))
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при декодировании JSON: " + str(e.msg))
        logger.error(f"Ответ сервера: " + str(response.text))
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
        "comment": "license activation",
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
        logger.info("Request: POST " + "\nparams: " + " \nheaders: " + str (headers) + " \ndata: " + str(json.dumps(menu_data)))
        response = requests.post(url, headers=headers, data=json.dumps(menu_data))
        logger.info("Response: " + str(response))
        response.raise_for_status()
        logger.info("JSON успешно отправлен. Код ответа:" + str(response.status_code))
        logger.info("Ответ сервера:" + str(response.json()))
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при отправке JSON: " + str(e.msg))
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON ответа: " + str(e.msg))

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
        logger.error(f"Ошибка при отправке запроса: " + str(e.msg))
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при декодировании JSON:" + str(e.msg))
        logger.error(f"Ответ сервера:" + str(response.text))
        return None