from seleniumbase import BaseCase

class Home(BaseCase):

    def test_basic(self):
        self.open('http://localhost:8000')
        self.click('.nav-link')
        current_url = self.get_current_url()
        self.assertTrue("login" in current_url)
        login_title = self.get_text("h1")
        self.assertTrue(login_title == "Log In")

class Login(BaseCase):

    def test_login(self):
        self.open('http://localhost:8000/accounts/login')
        self.update_text('#id_username', "test_user")
        self.update_text('#id_password', "testtest1")
        self.click('.btn-primary-new')
        self.wait_for_element_present("h1.text-left", timeout=10)
        title = self.get_text("h1")
        self.assertTrue(title == "Featured Event")

