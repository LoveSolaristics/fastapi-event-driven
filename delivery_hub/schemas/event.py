from event_type import EventType
from pydantic import BaseModel


class Event(BaseModel):
    event_type: EventType
    delivery_id: str
    data: dict
