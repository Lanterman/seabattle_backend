import uuid
import logging
import asyncio

from asgiref.sync import async_to_sync
from celery import shared_task

from config.utilities import redis_instance
from . import services


@shared_task
def countdown(lobby_slug: uuid, time_left: int, old_turn: str):
    """The task that acts like a countdown"""

    for number in range(time_left, -1, -1):
        current_turn = redis_instance.hget(lobby_slug, "current_turn")
        logging.info(msg=(current_turn, number))
        async_to_sync(asyncio.sleep)(1)

        if number > 0 and current_turn == old_turn:
            redis_instance.hset(lobby_slug, mapping={"time_left": number})

        else:
            if current_turn == "0":
                async_to_sync(asyncio.sleep)(5)
                if redis_instance.hget(lobby_slug, "current_turn") == "0":
                    services.determine_winner_at_preparation_stage(lobby_slug)
                    
            elif current_turn != None and number == 0:
                async_to_sync(asyncio.sleep)(3)
                services.determine_winner_at_shot_stage(lobby_slug)

            logging.info(msg="Task closed.")
            break
