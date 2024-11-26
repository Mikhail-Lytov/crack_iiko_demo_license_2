import sys
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

import src.create_new_document as create_new_document

def my_job(test_item, url_iiko, user_login, user_password):
    print("start license update time:", datetime.now())
    create_new_document.create_new_document(test_item, url_iiko, user_login, user_password)
    print("end license update time:", datetime.now())

def start_scheduler(test_item, url_iiko, user_login, user_password, number_days_scheduler):
    global scheduler
    try:
        scheduler = BlockingScheduler()
        print("Scheduler days: ", number_days_scheduler)
        scheduler.add_job(my_job, 'interval', weeks=0, days=number_days_scheduler, hours=0, minutes=0, seconds=0, args=[test_item, url_iiko, user_login, user_password])

        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("stop license update time:", datetime.now())
        print("error", sys.exc_info()[0])
        scheduler.shutdown()