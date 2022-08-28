from json import loads
from typing import Callable

from fastapi import HTTPException

from delivery_hub.db.models import Event
from delivery_hub.enums import DeliveryStatus, EventType


def create_delivery(
    _: dict[str, str | int],
    event: Event,
) -> dict[str, str | int]:
    data: dict[str, str | int] = loads(event.data)
    return {
        "id": event.delivery_id,
        "budget": int(data["budget"]),
        "notes": data["notes"],
        "status": DeliveryStatus.READY,
    }


def start_delivery(state: dict[str, str | int], _: Event) -> dict[str, str | int]:
    if state["status"] != "ready":
        raise HTTPException(status_code=400, detail="Delivery already started")

    return state | {"status": DeliveryStatus.ACTIVE}


def pickup_products(
    state: dict[str, str | int],
    event: Event,
) -> dict[str, str | int]:
    data = loads(event.data)
    old_budget: int = int(state["budget"])
    new_budget = old_budget - int(data["purchase_price"]) * int(data["quantity"])

    if new_budget < 0:
        raise HTTPException(status_code=400, detail="Not enough budget")

    return state | {
        "budget": new_budget,
        "purchase_price": int(data["purchase_price"]),
        "quantity": int(data["quantity"]),
        "status": DeliveryStatus.COLLECTED,
    }


def deliver_products(
    state: dict[str, str | int],
    event: Event,
) -> dict[str, str | int]:
    data: dict = loads(event.data)

    old_budget: int = int(state["budget"])
    new_budget: int = old_budget + int(data["sell_price"]) * int(data["quantity"])

    old_quantity: int = int(state["quantity"])
    new_quantity: int = old_quantity - int(data["quantity"])

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Not enough quantity")

    return state | {
        "budget": new_budget,
        "sell_price": int(data["sell_price"]),
        "quantity": new_quantity,
        "status": DeliveryStatus.COMPLETED,
    }


def increase_budget(
    state: dict[str, str | int],
    event: Event,
) -> dict[str, str | int]:
    data = loads(event.data)
    state["budget"] = int(data["budget"])
    return state


CONSUMERS: dict[EventType, Callable] = {
    EventType.CREATE_DELIVERY: create_delivery,
    EventType.START_DELIVERY: start_delivery,
    EventType.PICKUP_PRODUCTS: pickup_products,
    EventType.DELIVER_PRODUCTS: deliver_products,
    EventType.INCREASE_BUDGET: increase_budget,
}
