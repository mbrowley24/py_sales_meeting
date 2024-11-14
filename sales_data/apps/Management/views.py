from apps.authentication.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import View
from django.shortcuts import redirect, render
from django.urls import reverse
from utils.helper import generate_public_id
from .forms.SalesEngineerForm import SalesEngineerForm
from .forms.SalesRepForm import SalesRepForm
from utils.form_validation import username_regex, email_regex
from .helper_functions.sales_engineer_dto import get_sales_engineer_dto




class AssignSalesRepsToSalesEngineers(LoginRequiredMixin, View):
    template_name = "new_sales_reps.html"

    def get(self, request, id):

        form = SalesRepForm()

        try:
            user = User.objects.get(profile__public_id=id)

            form.set_sales_engineer(user)

            context = {'form': form}

            return render(request, self.template_name, context)

        except User.DoesNotExist:

            return redirect(reverse('apps.management:sales_engineers'))

class EditSalesEngineerView(LoginRequiredMixin, View):
        template_name = 'edit_sales_engineer.html'


        def get(self, request, id):



            try:
                sales_engineer = User.objects.get(profile__public_id=id)

                sales_engineer_data = {
                    "username" : sales_engineer.username,
                    "first_name" : sales_engineer.first_name,
                    "last_name" : sales_engineer.last_name,
                    "email" : sales_engineer.email,
                    "role" : sales_engineer.groups.all()[0],
                    "timezone": sales_engineer.profile.time_zone,
                    "regions": sales_engineer.profile.region,
                }

                form = SalesEngineerForm(initial=sales_engineer_data)

                context = {
                    'form': form,
                    'id' : id,
                }

                return render(request, self.template_name, context)

            except User.DoesNotExist:

                return redirect(reverse('apps.management:sales_engineers'))






class SalesEngineerView(LoginRequiredMixin, View):
    template_name = 'sales_engineer_table.html'

    #handle get request
    def get(self, request):

        sales_engineers = []
        user = request.user
        if user.is_superuser:

            sales_engineers = User.objects.filter(is_superuser=False)

        else:
            sales_engineers = User.objects.filter(profile__manager=user)


        sales_engineer_dtos = [get_sales_engineer_dto(sales_engineer) for sales_engineer in list(sales_engineers)]

        context = {
            'sales_engineers': sales_engineer_dtos
        }

        return render(request, self.template_name, context)


    def post(self, request):
        pass

class NewSalesEngineerView(LoginRequiredMixin, View):
    template_name = 'new_sales_engineer.html'
    form = SalesEngineerForm()


    #handle ger request
    def get(self, request):

        user  = request.user

        if not user.is_superuser:
            return "add redirect"


        context = {'form': self.form}

        return render(request, self.template_name, context)

    def post(self, request):
        self.form = SalesEngineerForm(request.POST)


        if self.form.is_valid():

            new_sales_engineer = User.objects.create(
                email=self.form.cleaned_data['email'],
                username=self.form.cleaned_data['username'],
                first_name=self.form.cleaned_data['first_name'],
                last_name=self.form.cleaned_data['last_name'],
                password=self.form.cleaned_data['password'],
            )

            new_sales_engineer.groups.add(self.form.cleaned_data['role'])
            new_sales_engineer.save()

            UserProfile.objects.create(
                public_id=generate_public_id(UserProfile),
                user=new_sales_engineer,
                manager=None,
                time_zone=self.form.cleaned_data['timezone'],
                region = self.form.cleaned_data['regions'],
            )


            return redirect(reverse('apps.management:sales_engineers'))


        context = {
            'form': self.form,
            'edit' : False,
        }
        return render(request, self.template_name, context)

@require_GET
@login_required(login_url='apps.authentication:login')
def check_username(request):

    #Get username for query param
    username = request.GET.get("username")
    id = request.GET.get("id")
    #response data
    response_data = {}

    #check the username passes regex required
    if username_regex(username):


        try:
            #Check username already exist
            user = User.objects.get(username=username)

            if id is None:
                response_data = {
                    "available": False,
                    "message" : "Username is already taken"
                }

            else:

                if id == user.profile.public_id:
                    print("here")
                    response_data = {
                        "available": True,
                        "message" : "current username"
                    }
                else:

                    response_data = {
                        "available": False,
                        "message": "Username is already taken"
                    }


        except User.DoesNotExist:

            #if username doesn't exist
            response_data = {
                "available": True,
                "message": "Username is available"
            }

    else:

        #username is not present or meets username standards
        response_data = {
            "available": False,
            "message" : "Username invalid"
        }


    return JsonResponse(response_data)

@require_GET
@login_required(login_url='apps.authentication:login')
def check_email(request):

    #get email from post
    email = request.GET.get('email')
    id = request.GET.get('id')

    response_data = {}

    if email_regex(email):

        try:
            user = User.objects.get(email=email)

            if id is None:

                response_data = {
                    "available": False,
                    "message" : "Email is already in use"
                }
            else:

                if id == user.profile.public_id:
                    response_data = {
                        "available": True,
                        "message": "available"
                    }
                else:
                    response_data = {
                        "available": False,
                        "message": "Email is already in use"
                    }

        except User.DoesNotExist:

            response_data = {
                "available": True,
                "message": "available"
            }

    else:
        response_data = {
            "available": False,
            "message" : "Email invalid"
        }

    return JsonResponse(response_data)