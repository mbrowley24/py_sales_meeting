from dataclasses import dataclass
from datetime import datetime
from apps.formData.models.timezone import Timezone

@dataclass
class SalesEngineerDTO:
    id : str
    first_name : str
    last_name : str
    email: str
    manager: str
    role: str
    timezone: str
    sales_reps: int
    last_login : datetime



def get_sales_engineer_dto(model) :

    manager = None
    region = None
    print(dict(model.__dict__))
    role = model.groups.all()


    if model.profile.manager is not None:

        manager = f"{model.profile.manager.first_name} {model.profile.manager.last_name}"

    if model.profile.region is not None:
        region = model.profile.region.name

    print(model.groups)

    return {
        "id":model.profile.public_id,
        "first_name":model.first_name,
        "last_name":model.last_name,
        "email":model.email,
        "manager": manager,
        "region": region,
        "role" : role[0].name,
        "sales_reps":model.sales_reps.count(),
        "last_login":model.last_login,

    }
