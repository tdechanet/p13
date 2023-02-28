from django.test import TestCase, Client
from unittest.mock import patch

from authentication.models import CustomUser, Following
from main.models import Program


class TestViewsMain(TestCase):

    def setUp(self):
        self.client = Client()

        self.user0 = CustomUser.objects.create_user(username="Test User0", email="test0@internet.net", password="secret")
        self.user1 = CustomUser.objects.create_user(username="Test User1", email="test1@internet.net", password="secret")
        self.following = Following.objects.create(author=self.user0, follower=self.user1)


        self.program_id = Program.objects.create(
            user_id=self.user0,
            name="Test Program",
            description="Test Description",
            published=0,
        ).pk

    # Test profile
    def test_profile_not_logged(self):
        response = self.client.get('/profile/')

        self.assertRedirects(response, '/login/?next=%2Fprofile%2F', status_code=302)

    def test_profile_logged(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['programs'][0].name, 'Test Program') #Check if the program is sent to template

    def test_profile_publish_unpublish_program(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post('/profile/', {'id':0, 'program_publish':'False'}) #Request publish

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Program.objects.get(id=self.program_id).published, True) #Test if program has been published

        response = self.client.post('/profile/', {'id':0, 'program_publish':'True'}) #Request unpublish

        self.assertEqual(Program.objects.get(id=self.program_id).published, False) #Test if program has been unpublished

    def test_profile_delete_program(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post('/profile/', {'id':0, 'program_delete':''}) #Request delete

        self.assertEqual(response.status_code, 302)
    

    # Test delete_program

    def test_delete_program_works(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.post(f'/program/{self.program_id}/delete/') #Request delete
        
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Program.DoesNotExist): #Check if error raises when getting program
            Program.objects.get(id=self.program_id)
    
    def test_delete_others_program(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.post(f'/program/{self.program_id}/delete/') #Request delete

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Program.objects.get(id=self.program_id).name, "Test Program") #Check if user can't delete others user program
