from apps.demo_data.models import TestProduct
from utils.helper import generate_public_id


#generate products if products does not exists
def generate_product_data(products):


    for product in products:

        try:

            TestProduct.objects.get(name = product)
            continue

        except TestProduct.DoesNotExist:

            TestProduct.objects.create(
                public_id = generate_public_id(TestProduct),
                name = product
            )


    return list(TestProduct.objects.all().order_by('name'))



