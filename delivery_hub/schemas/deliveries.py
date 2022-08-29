from pydantic import BaseModel, Extra, confloat

from delivery_hub.enums import DeliveryStatus


class CreateDeliveryRequest(BaseModel):
    budget: confloat(multiple_of=0.01, ge=0)  # type: ignore[valid-type]
    notes: str

    class Config:
        extra = Extra.forbid


class GetDeliveryStatus(BaseModel):
    id: str
    budget: confloat(multiple_of=0.01, ge=0)  # type: ignore[valid-type]
    notes: str
    status: DeliveryStatus
