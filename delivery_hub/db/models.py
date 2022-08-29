from json import dumps

from pydantic import conint, validator
from redis_om import HashModel

from delivery_hub.db.connection import redis
from delivery_hub.enums import EventType


class Delivery(HashModel):  # type: ignore[no-any-unimported]
    budget: conint(ge=0) = 0
    notes: str = ""

    class Meta:
        database = redis


class Event(HashModel):  # type: ignore[no-any-unimported]
    delivery_id: str
    type: EventType
    data: str

    @validator("data", pre=True)
    def data_validator(cls, data):
        if isinstance(data, dict):
            return dumps(data)
        return data

    class Meta:
        database = redis
