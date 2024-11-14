from select import select

from django import forms
from django.contrib.auth.models import User, Group
from django.db.models import Q
from apps.formData.models.timezone import Timezone
from apps.formData.models.division import Region
from utils.form_validation import email_regex, name_regex, username_regex

class SalesEngineerForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )

    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    email = forms.EmailField(

        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )


    timezone = forms.ModelChoiceField(
        queryset=Timezone.objects.all(),
        required=True,
        to_field_name='public_id',
        empty_label='Select Timezone',
    )

    regions = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        to_field_name='public_id',
        empty_label='Select Region',
    )





    def clean(self):
        clean_data = super().clean()

        username = clean_data['username']
        first_name = clean_data['first_name']
        last_name = clean_data['last_name']
        email = clean_data['email']


        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            print("exists by username error")
            self.add_error('username', f'Username {username} exist')

        if not username_regex(username):
            print("username_regex error")
            self.add_error('username', f'must be 3-50 alphanumeric characters')

        if 2 > len(first_name) or 100 < len(first_name):
            print("name_length error")
            self.add_error('first_name', f'must be 2-50 alphanumeric characters')

        if not name_regex(first_name):
            print("first_name_regex error")
            self.add_error("first_name", "must be 2-50 alphanumeric characters")

        if 2 > len(last_name) or 100 < len(last_name):
            print("name_length error")
            self.add_error('last_name', f'must be 2-50 alphanumeric characters')

        if not name_regex(last_name):
            print("last_name_regex error")
            self.add_error("last_name", "must be 2-50 alphanumeric characters")

        if not email_regex(email):
            print("email_regex error")
            self.add_error("email", "must contain a valid email address")


