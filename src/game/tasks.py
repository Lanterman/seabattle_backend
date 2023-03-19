import uuid
import logging
import asyncio

from asgiref.sync import async_to_sync
from celery import shared_task

from config.utilities import redis_instance


@shared_task
def countdown(lobby_slug: uuid, type_action: str):
    while True:
        time_left = int(redis_instance.hget(lobby_slug, type_action))
        logging.warning(msg=(lobby_slug, time_left, redis_instance.hget(lobby_slug, "done"), type_action))
        if redis_instance.hget(lobby_slug, "done") or time_left <= 0:
            break
        
        async_to_sync(asyncio.sleep)(1)
        redis_instance.hmset(lobby_slug, {type_action: time_left - 1})
