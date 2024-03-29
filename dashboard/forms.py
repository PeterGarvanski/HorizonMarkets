from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django.contrib.auth.models import User

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
