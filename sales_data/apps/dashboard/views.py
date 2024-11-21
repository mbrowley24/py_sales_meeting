from calendar import month
from datetime import datetime, timezone, timedelta
from itertools import product

from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render
from django.utils.timezone import make_aware

from apps.appointments.models import Appointment, AppointmentType
from apps.formData.models.products import Products
from apps.salesreps.models import SalesRepresentative


@login_required(login_url='apps.authentication:login')
def dashboard(request):

    #meeting data for the last year
    if request.method == 'GET':
        #get user and set the time frame
        user             = request.user
        year             = datetime.now().year
        start            = make_aware(datetime(year = year, month = 1, day = 1, hour = 0, minute = 0, second = 0))
        end              = make_aware(datetime(year = year, month = 12, day = 31, hour = 23, minute = 59, second = 59))

        #get appointments eager loading products, sale reps and meeting type
        appointments     = (Appointment.objects.filter(date__gte = start)
                            .filter(date__lte = end)
                            .filter(sales_engineer = user)
                            .prefetch_related('products__product')
                            .prefetch_related('sales_representative')
                            .prefetch_related('type')
                            ).order_by('date')


        appointment_data = []
        for appointment in appointments:
            product_strings   = []
            sales_rep         = f"{appointment.sales_representative.first_name} {appointment.sales_representative.last_name}"
            type_name         = appointment.type.name

            for product_obj in appointment.products.all():
                product_strings.append(product_obj.product.name)

            data_point = {
                "type"      : type_name,
                "date"      : appointment.date,
                "sales_rep" : sales_rep,
                "products"  : product_strings,
            }

            appointment_data.append(data_point)

        sales_reps      = SalesRepresentative.objects.filter(sales_engineer= user)

        sales_reps_names = []

        for sales_rep in sales_reps:
            sales_reps_names.append(f"{sales_rep.first_name} {sales_rep.last_name}")

        product_objs     = Products.objects.filter().order_by('name')

        product_names     = []

        for product_obj in product_objs:

            product_names.append(product_obj.name)

        appointment_types     = AppointmentType.objects.all()

        appointment_type_names = []

        for appointment_type in appointment_types:
            appointment_type_names.append(appointment_type.name)

        context = {
            'appointment_type_names': appointment_type_names,
            'appointment_data' : appointment_data,
            'sales_reps'       : sales_reps_names,
            'products'         : product_names,
        }

        return render(request, 'dashboard.html', context)




