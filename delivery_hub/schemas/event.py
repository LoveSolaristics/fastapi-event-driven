from pydantic import BaseModel

from delivery_hub.enums import EventType


class Event(BaseModel):
    delivery_id: str
    type: EventType
    data: dict
