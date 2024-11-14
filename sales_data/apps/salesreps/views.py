from django.shortcuts import render, redirect
from django.urls import reverse
from .models import SalesRepresentative
from django.contrib.auth.decorators import login_required
from .helper_functions import model_to_dataclass

@login_required(login_url='apps.authentication:login')
def sales_reps(request):

    user = request.user

    #if user is logged in
    if not user.is_authenticated:

        return redirect(reverse('apps.apps.authentication:login'))


    if request.method == 'GET':

        sales_representatives = SalesRepresentative.objects.filter(sales_engineer=user)

        sales_rep_dtos = [model_to_dataclass(model) for model in sales_representatives]

        context = {
            'sales_reps': sales_reps,
        }

        return render(request, 'sales_rep_table.html', context)


    else:
        return redirect(reverse('apps.apps.authentication:login'))

