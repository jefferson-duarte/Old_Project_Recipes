from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Novo test.')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Smith')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty.'
        },
        help_text=(
            'Password must have at least one uppercase letter, one lowercase letter and one number. The lenght should be at least 8 characters.'
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'The e-mail must be valid.',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty.',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your usename here',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atencao' in data:
            raise ValidationError(
                'Nao digite %(value)s no campo password.',
                code='Invalid',
                params={'value': '"atencao"'}
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'Jefferson Duarte' in data:
            raise ValidationError(
                'Nao digite %(value)s no campo first name.',
                code='Invalid',
                params={'value': '"Jefferson Duarte"'}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Password and password2 must be equal.'
            })
