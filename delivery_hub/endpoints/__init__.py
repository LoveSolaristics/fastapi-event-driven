from endpoints.v1 import routers_list_v1
from fastapi import APIRouter


routers_lists_with_prefixes: list[tuple[str, list[APIRouter]]] = [
    ("/api/v1", routers_list_v1),
]


__all__ = [
    "routers_lists_with_prefixes",
]
