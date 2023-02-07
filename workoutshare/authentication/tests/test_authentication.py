from django.test import TestCase, Client

from authentication.models import CustomUser


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()


    # Test signup
    def test_signup_method_get(self):
        response = self.client.get('/signup/')

        self.assertEqual(response.status_code, 200)

    def test_signup_method_post(self):
        user = CustomUser(id=1, username="martin", email="martin@internet.net", password = 'UltimatePassword56')
        response = self.client.post('/signup/', {
            'username':'martin',
            'email':'martin@internet.net', 
            'password1':'UltimatePassword56', 
            'password2':'UltimatePassword56'
        })

        self.assertRedirects(response, '/login/', status_code=302)
        self.assertEqual(CustomUser.objects.get(id = 1), user)
        
