from django import forms


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = '%m/%d/%Y %H:%M'
        super().__init__(**kwargs)

class AvailabilityForm(forms.Form):

    # ROOM_CATEGORIES = (
    #     ('BZS', 'BUSINESS SUITE'),
    #     ('TNS', 'TWIN SUITE'),
    #     ('EXS', 'EXECUTIVE SUITE'),
    #     ('SGB', 'SINGLE BED'),
    # )

    # category = forms.ChoiceField( choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'], widget=DateTimeInput)
    check_out = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'], widget=DateTimeInput)


class PhoneNoForm(forms.Form):

    phone_no = forms.IntegerField()