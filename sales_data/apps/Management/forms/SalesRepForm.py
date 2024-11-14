from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from apps.formData.models.timezone import Timezone
from apps.formData.models.division import Region
from apps.salesreps.models import SalesRepresentative, SalesRoles
from utils.form_validation import email_regex, name_regex, username_regex

class SalesRepForm(forms.Form):

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

    quota = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    sales_engineer = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Sales Engineer').all(),
        disabled=True,
    )

    role = forms.ModelChoiceField(
        queryset=SalesRoles.objects.all(),
        required=True,
        empty_label='Select Role',
    )




    def clean(self):
        clean_data = super().clean()

        first_name = clean_data['first_name']
        last_name = clean_data['last_name']
        email = clean_data['email']


        if 2 > len(first_name) or 100 < len(first_name):
            print("name_length error")
            self.add_error('first_name', f'must be 2-50 alphanumeric characters')

        if not name_regex(first_name):
            self.add_error("first_name", "must be 2-50 alphanumeric characters")

        if 2 > len(last_name) or 100 < len(last_name):
            self.add_error('last_name', f'must be 2-50 alphanumeric characters')

        if not name_regex(last_name):
            self.add_error("last_name", "must be 2-50 alphanumeric characters")

        if not email_regex(email):
            self.add_error("email", "must contain a valid email address")

        if SalesRepresentative.objects.filter(email=email).exists():
            self.add_error("email", "Email address already exists")




