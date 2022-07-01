from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_passord


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Smith')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    username = forms.CharField(
        label='Username',
        help_text='Username must have letters, numbers or one of those @.+-. The lenght should be between 4 and 150 characters.',
        error_messages={
            'required': 'This field must not be empty.',
            'min_length': 'Username must be have at least 4 characters.',
            'max_length': 'Username must have less than 150 characters.'
        },
        min_length=4,
        max_length=150,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name.'},
        required=True,
        label='First Name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name.'},
        required=True,
        label='Last Name'
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty.'
        },
        help_text=(
            'Password must have at least one uppercase letter, one lowercase letter and one number. The lenght should be at least 8 characters.'
        ),
        validators=[strong_passord],
        label='Password',
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages={
            'required': 'Please, reapet your password.'
        },
    )

    email = forms.EmailField(
        error_messages={'required': 'E-mail is required.'},
        label='E-mail',
        help_text='The e-mail must be valid.',
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Password and password2 must be equal.'
            })
