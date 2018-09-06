from seleniumbase import BaseCase
import time

host = 'http://localhost:8000'

"""
    Base test to see if test is working at all
"""

class Register(BaseCase):

    username = 'test_user3'
    email = 'testuser@testuser.com'
    password = 'test_userPASS'

    def test_register(self):
        self.open(host + '/register/')
        current_url = self.get_current_url()
        self.assertTrue("register" in current_url)
        login_title = self.get_text("h1")
        self.assertTrue(login_title == "Sign Up")
        self.update_text('#id_username', self.username)
        self.update_text('#id_email', self.email)
        self.update_text('#id_password', self.password)
        self.update_text('#id_password2', self.password)
        self.click('#tos')
        self.click('#submit')
        time.sleep(3)

    def test_user_exists(self):
        self.open(host + '/profiles/' + self.username)
        profile_title = self.get_text("h2")
        self.assertTrue(profile_title == self.username)


