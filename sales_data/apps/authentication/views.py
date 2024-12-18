from datetime                  import datetime
from django.contrib.auth       import logout
from django.shortcuts          import render, redirect
from django.urls               import reverse
from django.contrib.auth.forms import AuthenticationForm, User
from django.contrib.auth       import login, logout, authenticate
from django.utils.timezone     import make_aware

from apps.demo_data.models import TestAppointment, TestSalesEngineer, TestProduct, TestAppointmentType, TestOrganization


def app_login(request):


    if request.method == 'GET':

        form    = AuthenticationForm()

        context = {
            'form': form
        }

        return render(request, 'login.html', context)

    elif request.method == 'POST':

        form = AuthenticationForm(request, data = request.POST)

        #validate for data
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            #authenticate user
            user = authenticate(username = username,
                                password = password
                                )

            if user is not None:
                login(request, user)

                #check if superuser. If super go to sales rep table
                if user.is_superuser:

                    return redirect(reverse('apps.dashboard:dashboard'))

                else:
                    return redirect(reverse('apps.dashboard:dashboard'))




        else:
            context = {
                'form': form
            }

            return render(request, 'login.html', context)

    else:

        form = AuthenticationForm()

        context = {
            'form': form
        }

        return render(request, 'login.html', context)



def landing_page(request):

    if request.method == 'GET':
        year        = int(request.GET.get('year', datetime.now().year))
        user        = request.user
        start       = make_aware(datetime(year = year, month = 1, day = 1, hour = 0, minute = 0, second = 0))
        end         = make_aware(datetime(year = year, month = 12, day = 31, hour = 23, minute = 59, second = 59))

        organization_name = TestOrganization.objects.all()[0].name

        data = {
                 'sales_eng_mgr'  : {},
                 'products'       : [],
                 'meeting_types'  : []
                }


        products = TestProduct.objects.all()

        for product in products:

            data['products'].append(product.name)


        meeting_tags = TestAppointmentType.objects.all()

        for tag in meeting_tags:
            data['meeting_types'].append(tag.name)

        #capture sales engineers, sales engineer managers and sales reps
        sales_engineers = (TestSalesEngineer
                           .objects
                           .select_related("manager")
                           .prefetch_related('sales_reps')
                           .all())

        for sales_engineer in sales_engineers:

            manager_name   = f'{sales_engineer.manager.first_name} {sales_engineer.manager.last_name}'
            sales_eng_name = f'{sales_engineer.first_name} {sales_engineer.last_name}'

            if manager_name not in data['sales_eng_mgr']:

                data['sales_eng_mgr'][manager_name] = {
                    sales_eng_name: {}
                }

            else:

                data['sales_eng_mgr'][manager_name][sales_eng_name] = {}



            for sales_rep in sales_engineer.sales_reps.all():

                sales_rep_name = f'{sales_rep.first_name} {sales_rep.last_name}'

                data['sales_eng_mgr'][manager_name][sales_eng_name][sales_rep_name] = []


        appointments = (TestAppointment
                        .objects
                        .filter(date__gte = start, date__lte = end)
                        .select_related('type')
                        .select_related('customer')
                        .select_related('sales_engineer')
                        .select_related('sales_rep')
                        .prefetch_related('products')
                        )

        for appointment in appointments:

            type_name    = appointment.type.name
            sales_rep    = f'{appointment.sales_rep.first_name} {appointment.sales_rep.last_name}'
            sales_eng    = f'{appointment.sales_engineer.first_name} {appointment.sales_engineer.last_name}'
            prod_strings  = []

            for prod in appointment.products.all():

                prod_strings.append(prod.product.name)

            data_point = {

                "type"      : type_name,
                "customer"  : appointment.customer.name,
                "date"      : appointment.date,
                "sales_rep" : sales_rep,
                "products"  : prod_strings,

            }

            for mgr_name, sales_eng_obj in data['sales_eng_mgr'].items():

                if sales_eng in sales_eng_obj:

                    if sales_rep in data['sales_eng_mgr'][mgr_name][sales_eng]:

                        data['sales_eng_mgr'][mgr_name][sales_eng][sales_rep].append(data_point)

        print(organization_name)

        context = {
            'data'      : data,
            'org_name'  : organization_name
        }

        return render(request, 'landing_page.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('apps.authentication:login'))