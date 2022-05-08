from django import forms
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Submit


class ValidatorForm(forms.Form):
    qr_code = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'justify-content-center'
        self.helper.add_input(Submit('submit', 'Validate'))
