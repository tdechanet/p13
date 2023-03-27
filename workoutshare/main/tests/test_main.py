from django.test import TestCase, Client

from authentication.models import CustomUser, Following
from main.models import Program, Session, Exercice, MuscleGroup, Favorite


class TestViewsMain(TestCase):

    def setUp(self):
        self.client = Client()

        self.user0 = CustomUser.objects.create_user(username="Test User0", email="test0@internet.net", password="secret")
        self.user1 = CustomUser.objects.create_user(username="Test User1", email="test1@internet.net", password="secret")
        self.following0 = Following.objects.create(author=self.user0, follower=self.user1)

        self.program0 = Program.objects.create(
            user_id=self.user0,
            name="Test Program",
            description="Test Description",
            published=1,
        )

        self.program1 = Program.objects.create(
            user_id=self.user1,
            name="Test Program1",
            description="Test Description1",
            published=0,
        )

        self.favorite0 = Favorite.objects.create(
            user_id=self.user0,
            program_id=self.program1
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

#region home
    def test_home_followers(self):
        self.client.login(username='Test User1', password='secret') #Login
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["programs"][0], self.program0)

#endregion

#region legal_mention
    def test_legal_mention(self):
        response = self.client.get('/legal-mention/')

        self.assertEqual(response.status_code, 200)
#endregion

#region favorite
    def test_favorite_get(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.get('/favorite/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["favorites"][0], self.program1)

    def test_favorite_delete(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post('/favorite/', {'id':0})

        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Favorite.DoesNotExist): #Check if error raises when getting program
            Favorite.objects.get(id=self.favorite0.pk)
#endregion

#region profile
    def test_profile_not_logged(self):
        response = self.client.get('/profile/')

        self.assertRedirects(response, '/login/?next=%2Fprofile%2F', status_code=302) #Check that the program redirect to login

    def test_profile_logged(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['programs'][0].name, 'Test Program') #Check if the program is sent to template

    def test_profile_create_program(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post(f'/profile/{self.user0.pk}/', {'new_program':"", "name": "New Test Program"})

        self.assertEqual(response.status_code, 302)
        Program.objects.get(name="New Test Program") #Check if no error raises when getting following

    def test_profile_other_follow_unfollow(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post(f'/profile/{self.user1.pk}/', {'user_follow':""})

        self.assertEqual(response.status_code, 302)
        Following.objects.get(follower=self.user0) #Check if no error raises when getting following
 
        response = self.client.post(f'/profile/{self.user1.pk}/', {'user_follow':""})

        with self.assertRaises(Following.DoesNotExist): #Check if error raises when getting following
            Following.objects.get(follower=self.user0)

    def test_profile_other_add_delete_favorite(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post(f'/profile/{self.user1.pk}/', {'id':0, 'program_favorite':""})

        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Favorite.DoesNotExist): #Check if error raises when getting favorite
            Favorite.objects.get(id=self.favorite0.pk)
        
        response = self.client.post(f'/profile/{self.user1.pk}/', {'id':0, 'program_favorite':""})

        Favorite.objects.get(user_id=self.user0) #Check if no error raises when getting favorite

    def test_profile_unpublish_publish_program(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post('/profile/', {'id':0, 'program_publish':'True'}) #Request unpublish

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Program.objects.get(id=self.program0.pk).published, False) #Test if program has been unpublished

        response = self.client.post('/profile/', {'id':0, 'program_publish':'False'}) #Request publish

        self.assertEqual(Program.objects.get(id=self.program0.pk).published, True) #Test if program has been published

    def test_profile_delete_program(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post('/profile/', {'id':0, 'program_delete':''}) #Request delete

        self.assertEqual(response.status_code, 302) #Check if the program redirect to delete url
#endregion

#region delete_program
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
#endregion

#region program
    def test_program_not_logged(self):
        response = self.client.get(f'/program/{self.program0.pk}/')

        self.assertRedirects(response, f'/login/?next=%2Fprogram%2F{self.program0.pk}%2F', status_code=302) #Check that the program redirect to login

    def test_program_logged(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.get(f'/program/{self.program0.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sessions_list'][0][0], self.session0) #Check if the session is sent to template
        self.assertEqual(response.context['sessions_list'][0][1][0], self.exercice0) #Check if the exercices are sent to template

    def test_profile_create_session(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post(f'/program/{self.program0.pk}/', {'new_session':"", "name": "New Test Session"})

        self.assertEqual(response.status_code, 302)
        Session.objects.get(name="New Test Session") #Check if no error raises when getting new session

    def test_profile_modify_program_name(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post(f'/program/{self.program0.pk}/', {'modify_program_name':"", "name": "New Program Name"})

        self.assertEqual(response.status_code, 302)
        Program.objects.get(name="New Program Name") #Check if no error raises when getting program by his new name

    def test_program_delete_session(self):
        self.client.login(username='Test User0', password='secret') #Login
        response = self.client.post(f'/program/{self.program0.pk}/', {'id':0, 'session_delete':''}) #Request delete

        self.assertEqual(response.status_code, 302) #Check if the program redirect to delete url
#endregion

#region delete_session
    def test_delete_session_works(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.post(f'/session/{self.session0.pk}/delete/') #Request delete
        
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Session.DoesNotExist): #Check if error raises when getting session
            Session.objects.get(id=self.session0.pk)
    
    def test_delete_others_session(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.post(f'/session/{self.session0.pk}/delete/') #Request delete

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Session.objects.get(id=self.session0.pk).name, "Test Session") #Check if user can't delete others user session
#endregion

#region session
    def test_session_not_found(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.get('/session/1000/')

        self.assertEqual(response.status_code, 404)

    def test_session_not_owner(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.get(f'/session/{self.session0.pk}/', follow=True)

        self.assertEqual(response.status_code, 404)

    def test_session_get(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.get(f'/session/{self.session0.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["session"], self.session0)

    def test_session_delete_exercice(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.post(f'/session/{self.session0.pk}/', {"exercice_delete":"", "id":"0"})

        self.assertEqual(response.status_code, 302)

    def test_session_save_session(self):
        self.client.login(username='Test User0', password='secret')
        formset_dict = {
            'save_session':"",
            "name": "Test Session Modified",
            'form-INITIAL_FORMS': '1',
            'form-TOTAL_FORMS': '1',
            "form-0-id": f"{self.exercice0.pk}",
            "form-0-muscle_group_id": f"{self.muscle_group_id0.pk}",
            "form-0-name": "Test Exercice Modified",
            "form-0-sets": "1",
            "form-0-reps": "2",
            "form-0-cool": "2:00"
        }
        response = self.client.post(f'/session/{self.session0.pk}/', formset_dict)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Session.objects.filter(name="Test Session Modified").exists(), True)
        self.assertEqual(Exercice.objects.filter(name="Test Exercice Modified").exists(), True)
#endregion

#region delete_exercice
    def test_delete_exercice_works(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.post(f'/exercice/{self.exercice0.pk}/delete/') #Request delete
        
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Exercice.DoesNotExist): #Check if error raises when getting exercice
            Exercice.objects.get(id=self.exercice0.pk)
    
    def test_delete_others_exercice(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.post(f'/exercice/{self.exercice0.pk}/delete/') #Request delete

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Exercice.objects.get(id=self.exercice0.pk).name, "Test Exercice") #Check if user can't delete others user exercice
#endregion

#region new_exercice
    def test_new_exercice_not_found(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.get(f'/session/1000/exercice/')

        self.assertEqual(response.status_code, 404)

    def test_new_exercice_not_owner(self):
        self.client.login(username='Test User1', password='secret')
        response = self.client.get(f'/session/{self.session0.pk}/exercice/', follow=True)

        self.assertEqual(response.status_code, 404)

    def test_new_exercice_get(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.get(f'/session/{self.session0.pk}/exercice/')

        self.assertEqual(response.status_code, 200)
        
    def test_new_exercice_post(self):
        self.client.login(username='Test User0', password='secret')

        form_dict = {
            "muscle_group_id": f"{self.muscle_group_id0.pk}",
            "name": "Test New Exercice",
            "sets": "1",
            "reps": "2",
            "cool": "2:00"
        }
        response = self.client.post(f'/session/{self.session0.pk}/exercice/', form_dict)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Exercice.objects.filter(name="Test New Exercice").exists(), True)
#endregion

#region user_research
    def test_user_research(self):
        self.client.login(username='Test User0', password='secret')
        response = self.client.get(f'/research/', {"user_research_bar":"Test"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["users_details"][0][0], self.user1)
        self.assertEqual(response.context["users_details"][0][1], 1)
#endregion
