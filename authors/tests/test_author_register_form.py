from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


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
