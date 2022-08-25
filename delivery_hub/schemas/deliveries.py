from pydantic import BaseModel, Extra, confloat


class CreateDeliveryRequest(BaseModel):
    budget: confloat(multiple_of=0.01, ge=0)
    notes: str

    class Config:
        extra = Extra.forbid
