from json import dumps

from db.connection import redis
from db.models import Event
from fastapi import APIRouter, Body, Request
from schemas import Event as EventSchema
from utils.consumers import CONSUMERS
from utils.state import get_state


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
):
    state = get_state(event.delivery_id)
    event = Event(**event.dict()).save()
    new_state = CONSUMERS[event.type](state, event)
    redis.set(f"delivery:{event.delivery_id}", dumps(new_state))
    return new_state
