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
from utils.helper import generate_public_id, generate_random_string
from .forms.SalesEngineerForm import SalesEngineerForm
from .forms.SalesEngineerManagerForm import SalesEngineerManagerForm
from .forms.SalesRepForm import SalesRepForm
from utils.form_validation import username_regex, email_regex, value_cleaner
from .helper_functions.sales_engineer_dto import get_sales_engineer_dto, get_sales_engineer_manager_dto
from .tasks import EmailDataUserName, EmailDataPassword, send_username_new, send_password_new


class AssignSalesRepsToSalesEngineers(LoginRequiredMixin, View):
    template_name = "new_sales_reps.html"
    form          = SalesRepForm()

    def get(self, request, rep_id):

        # get user from the request
        auth_user = request.user

        # check if superuser
        if not auth_user.is_superuser:
            return redirect(reverse('apps.dashboard:dashboard'))


        try:
            user  = User.objects.get(profile__public_id=rep_id)
            # self.form.fields['sales_engineer'].initial = user

            self.form = SalesRepForm(sales_engineer=user, skip_sales_engineer=True)

            context = {'form'   : self.form,
                       'rep_id' : rep_id
                       }

            return render(request, self.template_name, context)

        except User.DoesNotExist:

            return redirect(reverse('apps.management:sales_engineers'))


    def post(self, request, rep_id):

        # get user from the request
        auth_user = request.user

        # check if superuser
        if not auth_user.is_superuser:
            return redirect(reverse('apps.dashboard:dashboard'))

        try:

            user      = User.objects.get(profile__public_id=rep_id)


            self.form = SalesRepForm(request.POST, skip_sales_engineer=True)



            if self.form.is_valid():


                SalesRepresentative.objects.create(
                    public_id      = generate_public_id(SalesRepresentative),
                    first_name     = self.form.cleaned_data.get('first_name'),
                    last_name      = self.form.cleaned_data.get('last_name'),
                    email          = self.form.cleaned_data.get('email'),
                    quota          = int(value_cleaner(self.form.cleaned_data['quota'])),
                    role           = self.form.cleaned_data.get('role'),
                    sales_engineer = user,
                )



            else:

                self.form.fields['sales_engineer'].initial = user
                context = {
                    'form'   : self.form,
                    'rep_id' : rep_id
                }
                return render(request, self.template_name, context)

        except User.DoesNotExist:

            print("sales engineer not found")

        return redirect(reverse('apps.management:sales_reps', kwargs={'rep_id': rep_id}))

class EditSalesEngineerView(LoginRequiredMixin, View):
        template_name = 'edit_sales_engineer.html'


        def get(self, request, rep_id):

            # get user from the request
            user = request.user

            # check if superuser
            if not user.is_superuser:
                return redirect(reverse('apps.dashboard:dashboard'))


            try:
                sales_engineer = User.objects.get(profile__public_id=rep_id)

                sales_engineer_data = {
                    "username"   : sales_engineer.username,
                    "first_name" : sales_engineer.first_name,
                    "last_name"  : sales_engineer.last_name,
                    "email"      : sales_engineer.email,
                    "role"       : sales_engineer.groups.all()[0],
                    "timezone"   : sales_engineer.profile.time_zone,
                    "regions"    : sales_engineer.profile.region,
                }

                form              = SalesEngineerForm(initial=sales_engineer_data)

                context = {
                    'form': form,
                    'id'  : id,
                }

                return render(request, self.template_name, context)

            except User.DoesNotExist:

                return redirect(reverse('apps.management:sales_engineers'))



class SalesRepresentativeView(LoginRequiredMixin, View):
    template_name = 'sales_reps_table.html'

    def get(self, request, rep_id):

        # get user from the request
        user = request.user

        # check if superuser
        if not user.is_superuser:
            return redirect(reverse('apps.dashboard:dashboard'))

        try:

            sales_rep_list      = []
            sales_engineer      = User.objects.get(profile__public_id=rep_id)
            assigned_sales_reps = sales_engineer.sales_reps.all()

            for sales_rep in assigned_sales_reps:

                # quota = sales_rep.quota/100
                sales_rep_list.append({
                    "id"             : sales_rep.public_id,
                    "first_name"     : sales_rep.first_name,
                    "last_name"      : sales_rep.last_name,
                    "email"          : sales_rep.email,
                    "role"           : sales_rep.role.name,
                    "sales_engineer" : f'{sales_engineer.first_name} {sales_engineer.last_name}',
                    "quota"          : sales_rep.quota,
                })

            context = {
                "id": rep_id,
                "sales_representatives": sales_rep_list,
            }


            return render(request, self.template_name, context)

        except User.DoesNotExist:
            pass





class NewSalesEngineerView(LoginRequiredMixin, View):
    template_name = 'new_sales_engineer.html'
    form          = SalesEngineerForm()



    #handle ger request
    def get(self, request):

        # get user from the request
        user = request.user

        # check if superuser
        if not user.is_superuser:
            return redirect(reverse('apps.dashboard:dashboard'))


        context = {'form': self.form}

        return render(request, self.template_name, context)

    #create a sales engineer
    def post(self, request):

        # get user from the request
        user = request.user

        # check if superuser
        if not user.is_superuser:
            return redirect(reverse('apps.dashboard:dashboard'))

        self.form              = SalesEngineerForm(request.POST)


        if self.form.is_valid():
            password           = generate_random_string(10)
            print(password)
            new_sales_engineer = User(
                email      = self.form.cleaned_data['email'].lower().strip(),
                username   = self.form.cleaned_data['username'].lower().strip(),
                first_name = self.form.cleaned_data['first_name'].lower().strip(),
                last_name  = self.form.cleaned_data['last_name'].lower().strip(),
            )

            group          = Group.objects.get(name="sales engineer")

            new_sales_engineer.set_password(password)
            new_sales_engineer.save()


            new_sales_engineer.groups.add(group)
            new_sales_engineer.save()

            UserProfile.objects.create(
                public_id = generate_public_id(UserProfile),
                user      = new_sales_engineer,
                manager   = self.form.cleaned_data['manager'],
                time_zone = self.form.cleaned_data['timezone'],
                region    = self.form.cleaned_data['regions'],
            )

            #email data to send to new user with username information only
            EmailDataUserName(
                sender    = "no-reply@yeomanswork.net",
                recipient = new_sales_engineer.email,
                name      = f'{new_sales_engineer.first_name} {new_sales_engineer.last_name}',
                username  = new_sales_engineer.username,
            )

            #email data to send password information to user
            EmailDataPassword(
                sender    = "no-reply@yeomanswork.net",
                recipient = new_sales_engineer.email,
                name      = f'{new_sales_engineer.first_name} {new_sales_engineer.last_name}',
                password  = password,
            )

            #send username email
            send_username_new(EmailDataUserName)

            #send username password
            send_password_new(EmailDataPassword)

            #redirect to sales engineers
            return redirect(reverse('apps.management:sales_engineers'))


        #here if form is not valid
        context = {
            'form' : self.form,
            'edit' : False,
        }
        return render(request, self.template_name, context)


class NewSalesEngineerManagerView(LoginRequiredMixin, View):
        template_name = "new_se_manager.html"
        form          = SalesEngineerManagerForm()

        #new sales manager form
        def get(self, request):

            user = request.user

            if not user.is_superuser:
                return redirect(reverse('apps.dashboard:dashboard'))



            context = {
                "form" : self.form,
            }

            return render(request, self.template_name, context)




        def post(self, request):
            self.form     = SalesEngineerManagerForm(request.POST)

            #get user from the request
            user = request.user

            #check if superuser
            if not user.is_superuser:
                return redirect(reverse('apps.dashboard:dashboard'))

            if self.form.is_valid():

                #ToDo remove this for development only
                password = generate_random_string(10)
                print(password)

                new_sales_engineer = User(
                    first_name     = self.form.cleaned_data['first_name'].lower().strip(),
                    last_name      = self.form.cleaned_data['last_name'].lower().strip(),
                    email          = self.form.cleaned_data['email'].lower().strip(),
                )
                new_sales_engineer.set_password(password)
                new_sales_engineer.save()

                manager_group     = Group.objects.get(name = 'sales engineer manager')

                new_sales_engineer.groups.add(manager_group)
                new_sales_engineer.save()

                UserProfile.objects.create(
                    user      = new_sales_engineer,
                    public_id = generate_public_id(UserProfile),
                    region    = self.form.cleaned_data['regions'],
                    time_zone = self.form.cleaned_data['timezone']
                )

                return redirect(reverse('apps.management:se_managers'))

            else:
                print("error")
                context = {
                    'form': self.form,
                }

                return render(request, self.template_name, context)




class SalesEngineerView(LoginRequiredMixin, View):
    template_name = 'sales_engineer_table.html'

    #handle get request
    def get(self, request):

        # get user from the request
        user = request.user

        # if user is not a superuser redirect
        if not user.is_superuser:
            return redirect(reverse('apps.dashboard:dashboard'))

        sales_engineers     = User.objects.filter(is_superuser=False).filter(groups__name="sales engineer")




        sales_engineer_dtos = [get_sales_engineer_dto(sales_engineer) for sales_engineer in list(sales_engineers)]

        context = {
            'sales_engineers' : sales_engineer_dtos
        }

        return render(request, self.template_name, context)


class SalesEngineerManagerView(LoginRequiredMixin, View):
    template_name = 'sales_engineer_managers.html'

    def get(self, request):

        #check if superuser
        user = request.user

        if not user.is_superuser:
            return redirect(reverse('apps.dashboard:dashboard'))

        sales_engineer_managers     = User.objects.filter(groups__name="sales engineer manager").all()

        sales_engineer_managers_dto = [get_sales_engineer_manager_dto(se) for se in sales_engineer_managers]


        context = {
            'sales_engineer_managers': sales_engineer_managers_dto
        }

        return render(request, self.template_name, context)




@require_GET
@login_required(login_url='apps.authentication:login')
def check_username(request):


    user = request.user

    #check if superuser
    if not user.is_superuser:

        return JsonResponse({
            "available": False,
            "message": "not authorized"
        })

    #Get username for query param
    username = request.GET.get("username")
    id = request.GET.get("id")
    #response data
    response_data = {}

    if username is None:

        return JsonResponse({
            "available": False,
            "message" : "Username invalid"
        })

    username_test = username.lower().strip()

    #check the username passes regex required
    if username_regex(username_test):


        try:
            #Check username already exist
            user = User.objects.get(username=username_test)

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

    user = request.user
    #check if superuser
    if not user.is_superuser:
        return JsonResponse({
            "available": False,
            "message": "not authorized"
        })

    #get email from post
    email = request.GET.get('email')
    id = request.GET.get('id')

    response_data = {}

    if email is None:
        return JsonResponse({
            "available": False,
            "message": "Email invalid"
        })

    email_test = email.lower().strip()

    if email_regex(email_test):

        try:
            user = User.objects.get(email=email_test)

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

@require_GET
@login_required(login_url='apps.authentication:login')
def check_sales_rep_email(request):

    #check if superuser
    user = request.user

    if not user.is_superuser:
        return JsonResponse({
            "available": False,
            "message": "not authorized"
        })


    email = request.GET.get('email')
    id = request.GET.get('id')
    response_data = {}

    if email is None:
        response_data = {
            "available": False,
            "message": "Email is already in use"
        }
        return JsonResponse(response_data)

    email_test = email.lower().strip()

    if email_regex(email_test):

        try:
            sales_rep = SalesRepresentative.objects.get(email=email_test)

            if id is None:

                response_data = {
                    "available": False,
                    "message": "Email is already in use"
                }
            else:

                if id == sales_rep.public_id:
                    response_data = {
                        "available": True,
                        "message": "available"
                    }
                else:
                    response_data = {
                        "available": False,
                        "message": "Email is already in use"
                    }

        except SalesRepresentative.DoesNotExist:

            response_data = {
                "available": True,
                "message": "available"
            }

    else:
        response_data = {
            "available": False,
            "message": "Email invalid"
        }

    return JsonResponse(response_data)
