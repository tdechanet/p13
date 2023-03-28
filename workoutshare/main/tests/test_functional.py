from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from authentication.models import CustomUser, Following
from main.models import Program, Session, Exercice, MuscleGroup, Favorite

class SeleniumTestCase(LiveServerTestCase):


    @classmethod
    def setUp(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()

        cls.user0 = CustomUser.objects.create_user(username="Test User0", email="test0@internet.net", password="secret")     

        cls.program0 = Program.objects.create(
            user_id=cls.user0,
            name="Test Program",
            description="Test Description",
            published=1,
        )

        cls.session0 = Session.objects.create(
            program_id = cls.program0,
            name = "Test Session"
        )

        cls.muscle_group_id0 = MuscleGroup.objects.create(
            name = "Test Muscle Group"
        )

        cls.exercice0 = Exercice.objects.create(
            session_id = cls.session0,
            muscle_group_id = cls.muscle_group_id0,
            name = "Test Exercice",
            sets = 1,
            reps = 2,
            cool = "2:00"
        )
    
    @classmethod
    def tearDown(cls):
        cls.selenium.quit()
        super().tearDownClass()

    
    def test_new_user(self):
        selenium = self.selenium
        #signup
        selenium.get('%s%s' % (self.live_server_url, '/signup/'))
        id_username = selenium.find_element(By.ID, 'id_username')
        id_email = selenium.find_element(By.ID, 'id_email')
        id_password1 = selenium.find_element(By.ID, 'id_password1')
        id_password2 = selenium.find_element(By.ID, 'id_password2')
        submit = selenium.find_element(By.ID, 'signup')

        id_username.send_keys('username')
        id_email.send_keys('email@mail.com')
        id_password1.send_keys('Exploboum')
        id_password2.send_keys('Exploboum')
        submit.send_keys(Keys.RETURN)

        #login
        id_username = selenium.find_element(By.ID, 'id_username')
        id_password = selenium.find_element(By.ID, 'id_password')
        submit = selenium.find_element(By.ID, 'login')

        id_username.send_keys('username')
        id_password.send_keys('Exploboum')
        submit.send_keys(Keys.RETURN)

        assert 'Accueil' in selenium.title

        #research user
        research_bar = selenium.find_element(By.NAME, 'user_research_bar')
        submit = selenium.find_element(By.ID, 'research_button')

        research_bar.send_keys('test')
        submit.click()

        assert 'Recherche' in selenium.title

        #get on other user profile, follow and favorite
        user_profile_link = selenium.find_element(By.CLASS_NAME, 'card-title')
        user_profile_link.click()
        
        assert 'Test User0' in selenium.title

        follow_button = selenium.find_element(By.NAME, 'user_follow')
        follow_button.click()

        favorite_button = selenium.find_element(By.CSS_SELECTOR, 'label.pointer-image')
        favorite_button.click()

        #get back on home page
        workoutshare_logo = selenium.find_element(By.XPATH, '//a[1]')
        selenium.execute_script("arguments[0].click();", workoutshare_logo)

        assert 'Test Program' in selenium.page_source

        #get on favorites page
        favorite_button = selenium.find_element(By.ID, 'favorite')
        favorite_button.click()

        assert 'Favoris' in selenium.title
        assert 'Test Program' in selenium.page_source

    def test_add_data(self):
        selenium = self.selenium
        #signup
        selenium.get('%s%s' % (self.live_server_url, '/login/'))

        #login
        id_username = selenium.find_element(By.ID, 'id_username')
        id_password = selenium.find_element(By.ID, 'id_password')
        submit = selenium.find_element(By.ID, 'login')

        id_username.send_keys('Test User0')
        id_password.send_keys('secret')
        submit.send_keys(Keys.RETURN)

        #go on profile page
        profile_logo = selenium.find_element(By.ID, 'profile')
        profile_logo.click()

        assert 'Test User0' in selenium.title

        #create new program
        modal_toggler_program = selenium.find_element(By.NAME, "new_program_modal")
        modal_toggler_program.click()

        input_program_name = selenium.find_element(By.ID, "id_name")
        new_program_button = selenium.find_element(By.NAME, "new_program")
    
        WebDriverWait(selenium, 20).until(EC.element_to_be_clickable(input_program_name)).send_keys('New Program')
        new_program_button.click()
        
        #create new session
        modal_toggler_session = selenium.find_element(By.NAME, "new_session_modal")
        modal_toggler_session.click()

        input_session_name = selenium.find_element(By.ID, "session_form")
        new_session_button = selenium.find_element(By.NAME, "new_session")

        WebDriverWait(selenium, 20).until(EC.element_to_be_clickable(input_session_name)).send_keys('New Session')
        new_session_button.click()

        #create new exercice
        new_exercice_button = selenium.find_element(By.CLASS_NAME, "btn-primary")
        new_exercice_button.click()

        input_exercice_name = selenium.find_element(By.ID, "id_name")
        input_muscle_group_id = selenium.find_element(By.ID, "id_muscle_group_id")
        validate_button = selenium.find_element(By.CLASS_NAME, "btn-primary")

        input_exercice_name.send_keys('New Exercice')
        input_muscle_group_id.send_keys('Test Muscle Group')
        validate_button.click()

        #validate_session
        validate_session = selenium.find_element(By.NAME, "save_session")
        validate_session.click()

        assert 'New Exercice' in selenium.page_source