import sys
import argparse


import scheduler.scheduler as scheduler

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Параметры запуска")
    parser.add_argument("--item_test", type=str, help="Поле для поиска", required=True)
    parser.add_argument("--url_iiko", type=str, help="url iiko", required=True)
    parser.add_argument("--url_login", type=str, help="Имя системного пользователя в iiko", required=True)
    parser.add_argument("--url_password", type=str, help="Пароль системного пользователя в iiko", required=True)

    args = parser.parse_args()

    TEST_ITEM = args.item_test
    URL_IIKO_BACKEND = args.url_iiko
    USER_LOGIN = args.url_login
    USER_PASSWORD = args.url_password
    scheduler.start_scheduler(TEST_ITEM, URL_IIKO_BACKEND, USER_LOGIN, USER_PASSWORD)