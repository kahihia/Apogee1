from seleniumbase import BaseCase

host = 'http://localhost:8000'

"""
    Base test to see if test is working at all
"""

class Home(BaseCase):

    def test_basic(self):
        # Basic test, get homepage and navigate to see if browser is working
        self.open(host)
        self.click('.nav-link')
        current_url = self.get_current_url()
        self.assertTrue("login" in current_url)
        login_title = self.get_text("h1")
        self.assertTrue(login_title == "Login")

class Login(BaseCase):

    def test_login(self):
        # Test that you can login 
        self.open(host + '/accounts/login')
        self.update_text('#id_username', "test_user")
        self.update_text('#id_password', "testtest1")
        self.click('.btn-primary-new')
        self.wait_for_element_present("h1.text-left", timeout=10)

