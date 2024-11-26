import argparse
import scheduler.scheduler as scheduler

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Параметры запуска")
    parser.add_argument("--item_test", type=str, help="Поле для поиска", required=True)
    parser.add_argument("--url_iiko", type=str, help="url iiko", required=True)
    parser.add_argument("--url_login", type=str, help="Имя системного пользователя в iiko", required=True)
    parser.add_argument("--url_password", type=str, help="Пароль системного пользователя в iiko", required=True)
    parser.add_argument("--number_days_scheduler", type=int, help="Количество дней перед запускам", required=True)

    args = parser.parse_args()

    scheduler.start_scheduler(args.item_test, args.url_iiko, args.url_login, args.url_password, args.number_days_scheduler)