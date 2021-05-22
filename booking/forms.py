from django import forms

class AvailabilityForm(forms.Form):

    # ROOM_CATEGORIES = (
    #     ('BZS', 'BUSINESS SUITE'),
    #     ('TNS', 'TWIN SUITE'),
    #     ('EXS', 'EXECUTIVE SUITE'),
    #     ('SGB', 'SINGLE BED'),
    # )

    # category = forms.ChoiceField( choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], required=True)
    check_out = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], required=True)


class PhoneNoForm(forms.Form):

    phone_no = forms.CharField(required=True)