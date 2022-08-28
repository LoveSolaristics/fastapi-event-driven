from json import dumps

from fastapi import APIRouter, Body, Request

from delivery_hub.db.connection import redis
from delivery_hub.db.models import Delivery, Event
from delivery_hub.event_type import EventType
from delivery_hub.schemas import CreateDeliveryRequest
from delivery_hub.utils.consumers import CONSUMERS
from delivery_hub.utils.state import get_state


api_router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"],
)


@api_router.post("/create")
async def create(
    _: Request,
    model: CreateDeliveryRequest = Body(...),
) -> dict[str, str | int]:
    delivery: Delivery = Delivery(budget=model.budget, notes=model.notes).save()
    event: Event = Event(delivery_id=delivery.pk, type=EventType.CREATE_DELIVERY, data=model.json()).save()
    state: dict[str, str | int] = CONSUMERS[event.type]({}, event)
    redis.set(f"delivery:{delivery.pk}", dumps(state))
    return state


@api_router.get("/{pk}/status")
async def get_delivery_status(
    pk: str,
) -> dict[str, str | int]:
    return get_state(pk)
