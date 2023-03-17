import time
import logging

from celery import shared_task

from config.utilities import redis_instance


@shared_task
def countdown(username: str, type_action: str):
    while True:
        time_left = int(redis_instance.hget(username, type_action))
        logging.warning((time_left, username))
        if redis_instance.hget(username, "done") or time_left == 0:
            break
        
        time.sleep(1)
        redis_instance.hmset(username, {type_action: time_left - 1})
