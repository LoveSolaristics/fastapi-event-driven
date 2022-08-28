from json import loads

import pytest
from redis import Redis
from starlette import status

from delivery_hub.enums import DeliveryStatus


class TestCreateDelivery:
    @pytest.mark.parametrize(
        "budget, notes, expected_status",
        (
            (2, "Two pizzas please", status.HTTP_201_CREATED),
            (0, "Free delivery", status.HTTP_201_CREATED),
            (1, "", status.HTTP_201_CREATED),
            (-1, "Give me some budget", status.HTTP_422_UNPROCESSABLE_ENTITY),
            (None, "Some non-budget delivery", status.HTTP_422_UNPROCESSABLE_ENTITY),
            (1, None, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ),
    )
    async def test_create_delivery(
        self, client, budget: int | None, notes: str | None, expected_status: int, redis_connection: Redis
    ):
        response = await client.post(
            "/api/v1/deliveries",
            json={
                "budget": budget,
                "notes": notes,
            },
        )
        assert response.status_code == expected_status, response.json()
        if expected_status == status.HTTP_201_CREATED:
            delivery_id = response.json()["id"]
            delivery_from_base = loads(redis_connection.get(f"delivery:{delivery_id}"))
            assert delivery_from_base["status"] == DeliveryStatus.READY
