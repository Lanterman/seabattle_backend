import time
import logging

from celery import shared_task

from config.utilities import redis_instance


@shared_task
def counddown(username: str, time_left: int, type_action: str):
    while True:
        logging.warning(time_left)
        if redis_instance.hget(username, "made_turn"):
            return True
        
        if time_left == 0:
            return False
        
        time.sleep(1)
        redis_instance.hmset(username, {type_action: time_left - 1})
        logging.warning(time_left)