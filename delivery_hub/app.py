import json

import consumers
from event_type import EventType
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel, get_redis_connection
from schemas.deliveries import CreateDeliveryRequest
from schemas.event import Event as EventSchema


app = FastAPI(
    title="DeliveryHub",
    description="Like DeliveryClub but better",
    docs_url="/swagger",
    openapi_url="/openapi",
    version="0.1.0",
)


app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])

redis = get_redis_connection(host="localhost", port="6379", password="sOmE_sEcUrE_pAsS", decode_responses=True)


class Delivery(HashModel):
    budget: int = 0
    notes: str = ""

    class Meta:
        database = redis


class Event(HashModel):
    delivery_id: str = None
    type: str
    data: str

    class Meta:
        database = redis


@app.get("/deliveries/{pk}/status")
async def get_state(
    pk: str,
):
    state = redis.get(f"delivery:{pk}")

    if state is not None:
        return json.loads(state)

    state = build_state(pk)
    redis.set(f"delivery:{pk}", json.dumps(state))
    return state


def build_state(pk: str):
    events = Event.find(Event.delivery_id == pk).all()
    state = {}

    for event in events:
        state = consumers.CONSUMERS[event.type](state, event)

    return state


@app.post("/deliveries/create")
async def create(
    _: Request,
    model: CreateDeliveryRequest = Body(...),
):
    delivery = Delivery(budget=model.budget, notes=model.notes).save()
    event = Event(delivery_id=delivery.pk, type=EventType.CREATE_DELIVERY, data=model.json()).save()
    state = consumers.CONSUMERS[event.type]({}, event)
    redis.set(f"delivery:{delivery.pk}", json.dumps(state))
    return state


@app.post("/event")
async def dispatch(
    _: Request,
    event: EventSchema = Body(...),
):
    state = await get_state(event.delivery_id)
    event = Event(**event.dict()).save()
    new_state = consumers.CONSUMERS[event.type](state, event)
    redis.set(f"delivery:{event.delivery_id}", json.dumps(new_state))
    return new_state
