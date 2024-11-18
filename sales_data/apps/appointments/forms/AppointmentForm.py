from django import forms


from apps.appointments.models import AppointmentType

from apps.salesreps.models import SalesRepresentative, SalesRoles
from utils.form_validation import date_pattern, time_pattern, text_regex

class AppointmentForm(forms.Form):

    time = forms.CharField(
        required = True,
        widget   = forms.TimeInput(
            format='%H:%M',
            attrs = {
                'type' : 'time',
                'class': 'form-control',
            }
        ),
        error_messages = {
            'required' : "time is required",
        }
    )

    date = forms.DateField(
        required = True,
        widget   = forms.DateInput(
                attrs = {
                    'type'  : 'date',
                    'class' : 'form-control',
                }
        ),
        error_messages={
            'required': "date is required",
        }

    )

    title = forms.CharField(
        max_length = 100,
        required   = True,
        widget     = forms.TextInput(

        ),
        error_messages={
            'required': "title is required",
        }
    )

    notes = forms.CharField(
        max_length = 255,
        required   = True,
        widget     = forms.Textarea(
            attrs = {

            }
        ),
        error_messages={
            'required': "notes is required",
        }
    )

    type = forms.ModelChoiceField(
        queryset = AppointmentType.objects.all(),
        required = True,
        empty_label = "Select Meeting Type",
        label = "Type",
        error_messages={
            'required': "type is required",
        }
    )

    sales_representative = forms.ModelChoiceField(

        queryset = SalesRepresentative.objects.all(),
        required=True,
        empty_label = "Select Sales Representative",
        error_messages={
            'required': "sales rep is required",
        }
    )




    def __init__(self, *args, **kwargs):
        sales_engineer = kwargs.pop('sales_engineer', None)
        skip_sales_rep = kwargs.pop('skip_sales_engineer', False)
        super(AppointmentForm, self).__init__(*args, **kwargs)


        if sales_engineer:

            sales_reps = SalesRepresentative.objects.filter(sales_engineer=sales_engineer)



            self.fields['sales_representative'].initial = sales_reps

        if skip_sales_rep:
            self.fields['sales_representative'].required = False


    def clean(self):
        clean_data = super().clean()
        print(clean_data)
        title = clean_data['title']
        notes = clean_data['notes']
        date  = clean_data['date']
        time  = clean_data['time']

        if not text_regex(notes):
            self.add_error('notes', "invalid character")

        if len(notes) > 255:
            self.add_error('notes', "must be 255 characters or less")

        if not text_regex(title):
            self.add_error('title', "invalid character")

        if len(title) > 255:
            self.add_error('title', "must be 255 characters or less")

        if not date:
            self.add_error('date', "required")

        if not time_pattern(time):
            self.add_error('time', "invalid character")









