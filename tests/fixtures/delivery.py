from pytest import fixture

from delivery_hub.db.models import Delivery, Event
from delivery_hub.enums import EventType, DeliveryStatus
from json import dumps


@fixture(scope='function')
def delivery(redis_connection) -> Delivery:
    budget = 1
    notes = "Some notes"
    delivery = Delivery(budget=budget, notes=notes).save()
    event = Event(
        delivery_id=delivery.pk,
        type=EventType.CREATE_DELIVERY,
        data=dumps({'budget': budget, 'notes': notes}),
        status=DeliveryStatus.READY,
    ).save()
    return delivery
