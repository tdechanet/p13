from django.test import TestCase, Client

from main.models import CustomUser, Program


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create(id=1, username="Test User", email="test@internet.net")
        self.user.set_password('secret')
        self.user.save()

        logged_in = self.client.login(username='Test User', password='secret')

        self.program = Program.objects.create(
            user_id=self.user,
            name="Test Program",
            description="Test Description",
            published=0,
        )

    # Test profile
    def test_profile(self):
        response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['followers'], 0)
        self.assertEqual(response.context['programs'][0].name, 'Test Program')
