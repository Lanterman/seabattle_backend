import uuid
import logging
import asyncio

from asgiref.sync import async_to_sync
from celery import shared_task

from config.utilities import redis_instance


@shared_task
def countdown(lobby_slug: uuid, type_action: str, my_turn: str):
    while True:
        time_left = int(redis_instance.hget(lobby_slug, type_action))
        current_turn = redis_instance.hget(lobby_slug, "current_turn")
        logging.warning(msg=(current_turn, my_turn, time_left, type_action))
        if current_turn != my_turn or time_left <= 0:
            break
        
        async_to_sync(asyncio.sleep)(1)
        redis_instance.hmset(lobby_slug, {type_action: time_left - 1})
