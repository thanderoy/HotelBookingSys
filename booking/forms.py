from django import forms


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = '%m/%d/%Y %H:%M'
        super().__init__(**kwargs)

class AvailabilityForm(forms.Form):

    check_in = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'], widget=DateTimeInput)
    check_out = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'], widget=DateTimeInput)


class PhoneNoForm(forms.Form):

    phone_no = forms.IntegerField()
    