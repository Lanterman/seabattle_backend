import uuid
import logging
import asyncio

from time import sleep
from asgiref.sync import async_to_sync
from celery import shared_task

from config.utilities import redis_instance


@shared_task
def countdown(lobby_slug: uuid, type_action: str, old_turn: str, time_left: int):
    """The task that acts like a countdown"""

    for number in range(time_left, 0, -1):
        current_turn = redis_instance.hget(lobby_slug, "current_turn")
        logging.info(msg=(old_turn, current_turn, number, type_action))
        if old_turn != current_turn or time_left <= 0:
            logging.info(msg="Task closed.")
            break
        
        async_to_sync(asyncio.sleep)(1)
        redis_instance.hmset(lobby_slug, {type_action: number})

