import requests
import json
import hashlib
from datetime import datetime, timedelta

def sha1_hash(string):
  """Вычисляет SHA-1 хеш строки."""
  sha1 = hashlib.sha1()
  sha1.update(string.encode('utf-8')) # Важно закодировать строку в байты
  return sha1.hexdigest()

def get_auth():
    url = "https://315-459-856.iiko.it/resto/api/auth"
    params = {
        "login": "user",
        "pass": sha1_hash("user#test"),
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.content.decode('utf-8')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None

def log_out(token):
    url = "https://315-459-856.iiko.it/resto/api/logout"

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
    url = "https://315-459-856.iiko.it/resto/api/v2/documents/menuChange"  #  Замените на ваш полный URL, если это не локальный endpoint

    params = {
        "dateFrom": date_from,
        "dateTo": date_to,
        #"revisionFrom": revision_from,
    }
    headers = {}
    headers["Cookie"] = 'key=' + token
    #if status:
     #   params["status"] = status

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Поднимает исключение для не-2xx кодов ответа

        data = response.json()

        #Обработка результата.  Предполагается JSON ответ.  Измените, если формат другой.
        print("Успешно получены данные:")
        print(json.dumps(data, indent=2)) #вывод отформатированного JSON

        # Извлечение максимальной ревизии (если она присутствует в ответе)
        if "revision" in data:
            max_revision = data["revision"]
            print(f"\nМаксимальная ревизия: {max_revision}")
            return max_revision
        else:
          print("\nМаксимальная ревизия не найдена в ответе.")
          return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        print(f"Ответ сервера: {response.text}") #вывод сырого ответа для отладки
        return None

def create_new_document(token, dateIncoming, dateTo, productId, price):
    url = "https://315-459-856.iiko.it/resto/api/v2/documents/menuChange"
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
        response.raise_for_status()  # Проверка на ошибки HTTP (4xx или 5xx)
        print("JSON успешно отправлен. Код ответа:", response.status_code)
        print("Ответ сервера:", response.json())  # Вывод ответа сервера для проверки
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке JSON: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON ответа: {e}")

def get_all_items(token):
    url = "https://315-459-856.iiko.it/resto/api/v2/entities/products/list?includeDeleted=false"
    headers = {}
    headers["Cookie"] = 'key=' + token
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
        print(f"Ответ сервера: {response.text}") #вывод сырого ответа для отладки
        return None

if __name__ == "__main__":
    # Пример использования:
    token = get_auth()
    today = datetime.now()
    yesterday = today - timedelta(days=30)
    today = today + timedelta(days=10)
    date_from = yesterday.strftime("%Y-%m-%d")
    date_to = today.strftime("%Y-%m-%d")

    print(get_all_items(token))

    max_revision = get_document_by_filet(date_from, date_to, token, status="approved") # Замените "approved" на нужный статус или оставьте None

    if max_revision is not None:
        print(f"\nИспользуйте {max_revision} в качестве revisionFrom в следующем запросе.")

    create_new_document(token)
    log_out(token)
    input("enter:")