from json import dumps

from db.connection import redis
from db.models import Delivery, Event
from event_type import EventType
from fastapi import APIRouter, Body, Request
from schemas import CreateDeliveryRequest
from utils.consumers import CONSUMERS
from utils.state import get_state


api_router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"],
)


@api_router.post("/create")
async def create(
    _: Request,
    model: CreateDeliveryRequest = Body(...),
):
    delivery = Delivery(budget=model.budget, notes=model.notes).save()
    event = Event(delivery_id=delivery.pk, type=EventType.CREATE_DELIVERY, data=model.json()).save()
    state = CONSUMERS[event.type]({}, event)
    redis.set(f"delivery:{delivery.pk}", dumps(state))
    return state


@api_router.get("/{pk}/status")
async def get_delivery_status(
    pk: str,
):
    return get_state(pk)
