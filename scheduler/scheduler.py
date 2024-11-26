import sys
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

import src.create_new_document as create_new_document

def my_job():
    print("start license update time:", datetime.now())
    create_new_document.create_new_document()
    print("end license update time:", datetime.now())

def start_scheduler():
    global scheduler
    try:
        scheduler = BlockingScheduler()
        scheduler.add_job(my_job, 'interval', weeks=0, days=0, hours=0, minutes=0, seconds=10)

        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("stop license update time:", datetime.now())
        print("error", sys.exc_info()[0])
        scheduler.shutdown()