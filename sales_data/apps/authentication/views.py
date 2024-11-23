from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, User
from django.contrib.auth import login, logout, authenticate



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


def logout_view(request):
    logout(request)
    return redirect(reverse('apps.authentication:login'))