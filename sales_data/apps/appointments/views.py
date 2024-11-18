from datetime import date, time, datetime, timedelta
from apps.authentication.models import UserProfile
from apps.salesreps.models import SalesRepresentative, SalesRoles
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import make_aware
from utils.helper import generate_public_id, generate_random_string
from utils.form_validation import username_regex, email_regex, value_cleaner
from .forms import AppointmentForm
from .models import Appointment

from ..salesreps.views import sales_reps



class AppointmentListView(LoginRequiredMixin, View):
    template_name = 'appointment_table.html'

    def get(self, request):
        past_days = request.GET.get('past_days', 30)
        user = request.user
        date_window = make_aware(datetime.now()) - timedelta(days=past_days)

        appointments  = Appointment.objects.filter(date__gte=date_window).filter(sales_engineer=user)

        appointment_list = []
        for appointment in appointments:

            time_string = appointment.date.time().replace(second=0, microsecond=0).strftime("%H:%M")
            appointment_data = {
                'time'      : time_string,
                'date'      : appointment.date.strftime("%Y-%m-%d"),
                'type'      : appointment.type.name,
                'title'     : appointment.title,
                'sales_rep' : f"{appointment.sales_representative.first_name} {appointment.sales_representative.last_name}",
            }

            appointment_list.append(appointment_data)

        context = {
            'appointment_list': appointment_list
        }

        return render(request, self.template_name, context)



class NewAppointmentView(LoginRequiredMixin, View):
    template_name = 'new_appointment.html'
    form          = AppointmentForm.AppointmentForm()

    def get(self, request):


        try:

            user      = User.objects.get(id=request.user.id)
            self.form = AppointmentForm.AppointmentForm(sales_engineer=user)

        except User.DoesNotExist:
            print("doesn't exists")


        context = {
            'form': self.form
        }

        return render(request, self.template_name, context)

    def post(self, request):

        self.form         = AppointmentForm.AppointmentForm(request.POST)
        user              = request.user


        if self.form.is_valid():

            split_time    = self.form.cleaned_data['time'].split(":")

            apt_date_time = datetime.combine(
                self.form.cleaned_data['date'],
                time(int(split_time[0]), int(split_time[1]))
            )

            Appointment.objects.create(
                public_id            = generate_public_id(Appointment),
                date                 = apt_date_time,
                title                = self.form.cleaned_data['title'],
                notes                = self.form.cleaned_data['notes'],
                type                 = self.form.cleaned_data['type'],
                sales_representative = self.form.cleaned_data['sales_representative'],
                sales_engineer       = user,
            )

            return redirect(reverse('apps.appointments:appointment_list'))

        else:
            print(self.form.errors)
            context = {
                'form': self.form
            }

            return render(request, self.template_name, context)

__all__ = ["AppointmentListView", "NewAppointmentView"]
