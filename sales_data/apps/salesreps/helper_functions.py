from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SalesRepSummary:
    id: str
    name: str
    sales_engineer: str
    role: str
    email: str
    quota: int
    updated_at: datetime



#create dataclass from model
def model_to_dataclass(model):

    return dict(
        id             = model.public_id,
        first_name     = model.first_name,
        last_name      = model.last_name,
        role           = model.role.name,
        email          = model.email,
        quota          = model.quota,
        updated_at     = model.updated_at,
    )