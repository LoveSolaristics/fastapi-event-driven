from json import dumps

from fastapi import APIRouter, Body, Request

from delivery_hub.db.connection import redis
from delivery_hub.db.models import Event
from delivery_hub.schemas import Event as EventSchema
from delivery_hub.utils.consumers import CONSUMERS
from delivery_hub.utils.state import get_state


api_router = APIRouter(
    prefix="/event",
    tags=["Events"],
)


@api_router.post(
    "",
)
async def dispatch(
    _: Request,
    event: EventSchema = Body(...),
) -> dict[str, str | int]:
    state: dict[str, str | int] = get_state(event.delivery_id)
    new_event: Event = Event(**event.dict()).save()
    new_state: dict[str, str | int] = CONSUMERS[new_event.type](state, new_event)
    redis.set(f"delivery:{new_event.delivery_id}", dumps(new_state))
    return new_state
