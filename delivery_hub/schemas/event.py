from pydantic import BaseModel

from delivery_hub.event_type import EventType


class Event(BaseModel):
    event_type: EventType
    delivery_id: str
    data: dict
