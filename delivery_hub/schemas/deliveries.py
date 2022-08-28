from pydantic import BaseModel, confloat, Extra


class CreateDeliveryRequest(BaseModel):
    budget: confloat(multiple_of=0.01, ge=0)  # type: ignore[valid-type]
    notes: str

    class Config:
        extra = Extra.forbid
