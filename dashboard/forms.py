from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django.contrib.auth.models import User
from .models import Transaction

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {
            'username': '',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'User Profile Information',
                'username',
                'email',
                'first_name',
                'last_name'
            ),
            Submit('submit', 'Save', css_class='btn btn-primary save')
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-inputs'
            field.widget.attrs['id'] = field_name
            self.fields[field_name].label = f'<span class="form-label">{self.fields[field_name].label}</span>'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'country',
            'city',
            'postal_code',
            'address_line_1',
            'amount',
            'transfer_type',
        ]

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Transaction Details',
                'amount',
                'transfer_type',
            ),
            Fieldset(
                'Billing Address',
                'country',
                'city',
                'postal_code',
                'address_line_1'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary save')
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-inputs-transaction'
            field.widget.attrs['id'] = field_name
            self.fields[field_name].label = f'<span class="form-label-transaction">{self.fields[field_name].label}</span>'
            
            if field_name in ['country', 'city', 'postal_code', 'address_line_1']:
                field.initial = None
