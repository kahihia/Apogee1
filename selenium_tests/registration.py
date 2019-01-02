from seleniumbase import BaseCase
import time
from login import login, fan_login
import pytest

host = 'http://localhost:8000'

"""
    Base test to see if test is working at all
"""

def register(self):
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
    time.sleep(1)
    self.wait_for_element_present("h1.text-left", timeout=5)

def fan_register(self):
    self.open(host + '/register/')
    current_url = self.get_current_url()
    self.assertTrue("register" in current_url)
    login_title = self.get_text("h1")
    self.assertTrue(login_title == "Sign Up")
    self.update_text('#id_username', self.fan_username)
    self.update_text('#id_email', self.fan_email)
    self.update_text('#id_password', self.fan_password)
    self.update_text('#id_password2', self.fan_password)
    self.click('#tos')
    self.click('#submit')
    time.sleep(1)
    self.wait_for_element_present("h1.text-left", timeout=5)

def unregister(self):
    login(self)
    self.open(host + '/profiles/' + self.username + '/unregister/')
    page_heading = self.get_text("h1")
    self.assertTrue(page_heading == "Unregister")
    self.click('.btn-danger')
    page_heading = self.get_text("h1")
    self.assertTrue(page_heading == "Account Deleted")

def fan_unregister(self):
    fan_login(self)
    self.open(host + '/profiles/' + self.fan_username + '/unregister/')
    page_heading = self.get_text("h1")
    self.assertTrue(page_heading == "Unregister")
    self.click('.btn-danger')
    page_heading = self.get_text("h1")
    self.assertTrue(page_heading == "Account Deleted")


class Register(BaseCase):

    username = 'test_user3'
    email = 'testuser@testuser.com'
    password = 'test_userPASS'

    @pytest.mark.run(order=1)
    def test_register(self):
        register(self)

    @pytest.mark.run(order=2)
    def test_user_exists(self):
        login(self)
        self.open(host + '/profiles/' + self.username)
        profile_title = self.get_text("h2")
        self.assertTrue(profile_title == self.username)
    
    @pytest.mark.run(order=3)
    def test_delete_user(self):
        unregister(self)

