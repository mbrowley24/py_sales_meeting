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



def get_sales_engineer_dto(model):

    manager = None
    region = None
    role = model.groups.all()


    if model.profile.manager is not None:

        manager = f"{model.profile.manager.first_name} {model.profile.manager.last_name}"

    if model.profile.region is not None:
        region = model.profile.region.name



    return {
        "id":model.profile.public_id,
        "first_name":model.first_name,
        "last_name":model.last_name,
        "email":model.email,
        "manager": manager,
        "region": region,
        "sales_reps":model.sales_reps.count(),
        "last_login":model.last_login,

    }

def get_sales_engineer_manager_dto(model):

    region = None
    print(model)

    if model.profile.region is not None:
        region = model.profile.region.name

    print(model.sales_engineers.count())

    return {
        "id": model.profile.public_id,
        "first_name": model.first_name,
        "last_name": model.last_name,
        "email": model.email,
        "region": region,
        "sales_engineers": model.sales_engineers.count(),
        "last_login": model.last_login,

    }