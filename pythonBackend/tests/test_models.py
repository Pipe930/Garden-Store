from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):

    def test_create_user(self):
        # Test que comprueba si el usuario se creo correctamente

        first_name = 'test'
        last_name = 'test'
        email = 'test@gmail.com'
        username = 'test1'
        password = 'test1234'

        user = get_user_model().objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            password = password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        # Test que comprueba la normalizacion del correo electronico

        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(
            'test', email, 'test', 'test1234'
            )

        self.assertEqual(user.email, email.lower())
    
    def test_create_superuser(self):
        # Test que comprueba si se creo un super usuario correctamente

        first_name = 'admin'
        last_name = 'admin'
        email = 'admin@gmail.com'
        username = 'admin1'
        password = 'admin1234'

        user = get_user_model().objects.create_superuser(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
            password = password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)