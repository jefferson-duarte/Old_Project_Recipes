# from django.test import TestCase
import django
from authors.forms import RegisterForm
from parameterized import parameterized
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ('username', 'Your username'),
            ('email', 'Your email'),
            ('first_name', 'Ex.: John'),
            ('last_name', 'Ex.: Smith'),
            ('password', 'Type your password'),
            ('password2', 'Repeat your password'),
        ]
    )
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [
            ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),
            ('email', 'The e-mail must be valid.'),
            ('password',
                'Password must have at least one uppercase letter, one lowercase letter and one number. The lenght should be at least 8 characters.'
             ),
        ]
    )
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current_placeholder = form[field].field.help_text
        self.assertEqual(current_placeholder, needed)

    @parameterized.expand(
        [
            ('username', 'Username'),
            ('first_name', 'First Name'),
            ('last_name', 'Last Name'),
            ('email', 'E-mail'),
            ('password', 'Password'),
            ('password2', 'Password2'),
        ]
    )
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current_placeholder = form[field].field.label
        self.assertEqual(current_placeholder, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty.'),
        ('first_name', 'Write your first name.'),
        ('last_name', 'Write your last name.'),
        ('password', 'Password must not be empty.'),
        ('password2', 'Please, reapet your password.'),
        ('email', 'E-mail is required.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
