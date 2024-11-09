from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SalesRepSummary:
    id: str
    name: str
    sales_engineer: str
    role: str
    phone: str
    email: str
    quota: int
    updated_at: datetime



#create dataclass from model
def model_to_dataclass(model):

    return SalesRepSummary(
        id=model.public_id,
        name= f"{model.first_name} {model.last_name}",
        sales_engineer= f"{model.first_name} {model.last_name}",
        role= model.role.name,
        phone= model.phone,
        email= model.email,
        quota= model.quota,
        updated_at=model.updated_at,
    )