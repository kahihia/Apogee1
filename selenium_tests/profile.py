from seleniumbase import BaseCase
import time

host = 'http://localhost:8000'

"""
    Base test to see if test is working at all
"""

class Profile(BaseCase):

    username = 'test_user3'
    email = 'testuser@testuser.com'
    password = 'test_userPASS'

    def test_login(self):
        # Test that you can login 
        self.open(host + '/accounts/login')
        self.update_text('#id_username', self.username)
        self.update_text('#id_password', self.password)
        self.click('.btn-primary-new')
        self.wait_for_element_present("h1.text-left", timeout=10)

    def test_following_tab_on_login(self):
        # Test that you can login 
        self.open(host + '/accounts/login')
        self.update_text('#id_username', self.username)
        self.update_text('#id_password', self.password)
        self.click('.btn-primary-new')
        self.assert_element(".home-nav ul > li > a.active", timeout=10)
        highlighted_events_section = self.get_text(".home-nav a.active")
        self.assertTrue(highlighted_events_section == 'FOLLOWING')


    def test_user_exists(self):
        self.open(host + '/profiles/' + self.username)
        profile_title = self.get_text("h2")
        self.assertTrue(profile_title == self.username)


