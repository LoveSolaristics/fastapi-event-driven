from enum import Enum


class EventType(str, Enum):
    CREATE_DELIVERY = "create_delivery"
    START_DELIVERY = "start_delivery"
    PICKUP_PRODUCTS = "pickup_products"
    DELIVER_PRODUCTS = "deliver_products"
    INCREASE_BUDGET = "increase_budget"


class DeliveryStatus(str, Enum):
    READY = "ready"
    ACTIVE = "active"
    COLLECTED = "collected"
    COMPLETED = "completed"
