from redis import Redis
from redis_om import get_redis_connection

from delivery_hub.config import get_settings


settings = get_settings()
redis: Redis = get_redis_connection(
    host=settings.APP_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)
