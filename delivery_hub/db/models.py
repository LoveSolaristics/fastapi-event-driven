from redis_om import HashModel

from delivery_hub.db.connection import redis
from delivery_hub.event_type import EventType


class Delivery(HashModel):  # type: ignore[no-any-unimported]
    budget: int = 0
    notes: str = ""

    class Meta:
        database = redis


class Event(HashModel):  # type: ignore[no-any-unimported]
    delivery_id: str
    type: EventType
    data: str

    class Meta:
        database = redis
