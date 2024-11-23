from django import forms
from django.contrib.auth.models import User
from apps.formData.models.Vertical import Vertical
from apps.salesreps.models import SalesRepresentative
from utils.form_validation import name_regex, text_regex


class CustomerForm(forms.Form):

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    notes = forms.CharField(
        widget = forms.Textarea(
            attrs = {'class': 'form-control'}
        )
    )

    sales_rep = forms.ModelChoiceField(
        queryset    = SalesRepresentative.objects.all(),
        required    = True,
        empty_label = "Choose a Sales Representative",
    )

    vertical = forms.ModelChoiceField(
        queryset = Vertical.objects.all(),
        required = True,
        empty_label = "Choose a Vertical"
    )

    sales_engineer = forms.ModelChoiceField(
        queryset = User.objects.filter(groups__name='sales engineer').all(),
        required = True,
        empty_label = "Choose a Sales Engineer",
    )


    def __init__(self, *args, **kwargs):
        sales_engineer = kwargs.pop('sales_engineer', None)
        skip_sales_engineer = kwargs.pop('skip_sales_engineer', False)
        super(CustomerForm, self).__init__(*args, **kwargs)

        if sales_engineer:

            self.fields['sales_engineer'].initial = sales_engineer

        if skip_sales_engineer:

            self.fields['sales_engineer'].required = False


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        notes = cleaned_data['notes']


        if len(notes) > 255:
            self.add_error('notes', f'Your notes can have at most 255 characters')

        if not text_regex(notes):
            self.add_error('notes', 'invalid characters')

        if len(name) > 100:
            self.add_error('name', f'Name can have at most 100 characters')

        if not name_regex(name):
            self.add_error('name', "invalid characters")



