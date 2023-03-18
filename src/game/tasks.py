import logging
import asyncio

from asgiref.sync import async_to_sync
from celery import shared_task

from config.utilities import redis_instance


@shared_task(trail=True)
def countdown(username: str, type_action: str):
    while True:
        time_left = int(redis_instance.hget(username, type_action))
        logging.warning(msg=(username, time_left, redis_instance.hget(username, "done"), type_action))
        if redis_instance.hget(username, "done") or time_left <= 0:
            break
        
        async_to_sync(asyncio.sleep)(1)
        redis_instance.hmset(username, {type_action: time_left - 1})
