from django import forms
from datetime import datetime



class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    attrs = {
        'min': '0'
        }
    def __init__(self, **kwargs):
        kwargs["format"] = '%m/%d/%Y %H:%M'
        super().__init__(**kwargs)

class AvailabilityForm(forms.Form):
    
    today_date = datetime.now()
    iso_date = today_date.strftime('%Y-%m-%dT%H:%M')

    check_in = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'], widget=DateTimeInput(attrs={'min': iso_date}))
    check_out = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'], widget=DateTimeInput(attrs={'min': iso_date}))


class PhoneNoForm(forms.Form):

    phone_no = forms.IntegerField()
    