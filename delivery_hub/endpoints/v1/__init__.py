from endpoints.v1.deliveries import api_router as deliveries_api_router
from endpoints.v1.events import api_router as events_api_router


routers_list_v1 = [
    events_api_router,
    deliveries_api_router,
]


__all__ = [
    "routers_list_v1",
]
