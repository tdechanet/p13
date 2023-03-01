from django.test import TestCase, Client

from authentication.models import CustomUser, Following
from main.models import Program, Session, Exercice, MuscleGroup


class TestViewsMain(TestCase):

    def setUp(self):
        self.client = Client()

        self.user0 = CustomUser.objects.create_user(username="Test User0", email="test0@internet.net", password="secret")
        self.user1 = CustomUser.objects.create_user(username="Test User1", email="test1@internet.net", password="secret")
        self.following = Following.objects.create(author=self.user0, follower=self.user1)

        self.program0 = Program.objects.create(
            user_id=self.user0,
            name="Test Program",
            description="Test Description",
            published=0,
        )

        self.session0 = Session.objects.create(
            program_id = self.program0,
            name = "Test Session"
        )

        self.muscle_group_id0 = MuscleGroup.objects.create(
            name = "Test Muscle Group"
        )

        self.exercice0 = Exercice.objects.create(
            session_id = self.session0,
            muscle_group_id = self.muscle_group_id0,
            name = "Test Exercice",
            sets = 1,
            reps = 2,
            cool = "2:00"
        )

    # Test profile
    def test_profile_not_logged(self):
        response = self.client.get('/profile/')

        self.assertRedirects(response, '/login/?next=%2Fprofile%2F', status_code=302) #Check that the program redirect to login

    def test_profile_logged(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['programs'][0].name, 'Test Program') #Check if the program is sent to template

    def test_profile_publish_unpublish_program(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post('/profile/', {'id':0, 'program_publish':'False'}) #Request publish

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Program.objects.get(id=self.program0.pk).published, True) #Test if program has been published

        response = self.client.post('/profile/', {'id':0, 'program_publish':'True'}) #Request unpublish

        self.assertEqual(Program.objects.get(id=self.program0.pk).published, False) #Test if program has been unpublished

    def test_profile_delete_program(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post('/profile/', {'id':0, 'program_delete':''}) #Request delete

        self.assertEqual(response.status_code, 302) #Check if the program redirect to delete url


    # Test delete_program
    def test_delete_program_works(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.post(f'/program/{self.program0.pk}/delete/') #Request delete
        
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Program.DoesNotExist): #Check if error raises when getting program
            Program.objects.get(id=self.program0.pk)

    def test_delete_others_program(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.post(f'/program/{self.program0.pk}/delete/') #Request delete

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Program.objects.get(id=self.program0.pk).name, "Test Program") #Check if user can't delete others user program


    # Test program
    def test_program_not_logged(self):
        response = self.client.get(f'/program/{self.program0.pk}/')

        self.assertRedirects(response, '/login/?next=%2Fprogram%2F10%2F', status_code=302) #Check that the program redirect to login

    def test_program_logged(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.get(f'/program/{self.program0.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sessions']["Test Session"][0], self.exercice0) #Check if the session is sent to template

    def test_program_delete_session(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post(f'/program/{self.program0.pk}/', {'id':0, 'session_delete':''}) #Request delete

        self.assertEqual(response.status_code, 302) #Check if the program redirect to delete url

    # Test delete_session
    def test_delete_session_works(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.post(f'/session/{self.session0.pk}/delete/') #Request delete
        
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Session.DoesNotExist): #Check if error raises when getting session
            Session.objects.get(id=self.session0.pk)
    
    def test_delete_others_program(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.post(f'/session/{self.session0.pk}/delete/') #Request delete

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Session.objects.get(id=self.session0.pk).name, "Test Session") #Check if user can't delete others user session
