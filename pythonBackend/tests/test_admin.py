from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            first_name = 'admin', 
            last_name = 'admin', 
            username = 'admin1', 
            email = 'admin@gmail.com', 
            password = 'admin1234'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            first_name = 'user', 
            last_name = 'user', 
            username = 'user1', 
            email = 'user@gmail.com', 
            password = 'auser1234'
        )
    
    def test_user_listed(self):
        url = reverse('users')
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)
    
    def test_user_change_page(self):
        url = reverse('user', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)