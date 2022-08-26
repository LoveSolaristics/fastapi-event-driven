from json import dumps, loads

from db.connection import redis
from db.models import Event
from utils.consumers import CONSUMERS


def build_state(pk: str):
    events = Event.find(Event.delivery_id == pk).all()
    state = {}

    for event in events:
        state = CONSUMERS[event.type](state, event)
    return state


def get_state(pk: str) -> "str":
    state = redis.get(f"delivery:{pk}")

    if state is not None:
        return loads(state)

    state = build_state(pk)
    redis.set(f"delivery:{pk}", dumps(state))
    return state
