import redis
from . import settings


redis_instance = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    decode_responses=True,
    encoding="utf-8",
    )


def column_generate(column_name: str) -> str:
    """Generate a string as a dictionary"""

    return str({f"{column_name}{element}": "" for element in range(1, 11)})
