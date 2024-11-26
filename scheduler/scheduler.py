import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import src.create_new_document as create_new_document

logger = logging.getLogger()

def log():
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('crack_iikoRMS_demo_license.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

def my_job(test_item, url_iiko, user_login, user_password):
    logger.info("start license update time:" + str(datetime.now()))
    create_new_document.create_new_document(test_item, url_iiko, user_login, user_password)
    logger.info("end license update time:" + str(datetime.now()))

def start_scheduler(test_item, url_iiko, user_login, user_password, number_days_scheduler):
    log()
    global scheduler
    try:
        scheduler = BlockingScheduler()
        logger.info("Scheduler days: " + str(number_days_scheduler))
        scheduler.add_job(my_job, 'interval', weeks=0, days=number_days_scheduler, hours=0, minutes=0, seconds=10, args=[test_item, url_iiko, user_login, user_password])

        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.error("stop license update time:" + str(datetime.now()))
        logger.error("error" + str(sys.exc_info()[0]))
        scheduler.shutdown()