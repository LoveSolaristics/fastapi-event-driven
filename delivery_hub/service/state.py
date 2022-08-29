from json import dumps, loads

from delivery_hub.db.connection import redis
from delivery_hub.db.models import Event
from delivery_hub.service.consumers import CONSUMERS


def build_state(pk: str) -> dict[str, str | int]:
    print('pk', pk)
    events = Event.find(Event.delivery_id == pk).all()
    print('events', events)
    state: dict[str, str | int] = {}

    for event in events:
        state = CONSUMERS[event.type](state, event)
    return state


def get_state(pk: str) -> dict[str, str | int]:
    state: str | None = redis.get(f"delivery:{pk}")
    print('state', state)
    if state is not None:
        unpacked_state: dict[str, str | int] = loads(state)
        return unpacked_state
    built_state: dict[str, str | int] = build_state(pk)
    print('built_state', built_state)
    redis.set(f"delivery:{pk}", dumps(built_state))
    return built_state
