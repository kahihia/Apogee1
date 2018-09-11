from seleniumbase import BaseCase
import time
from registration import register, unregister
from login import login
import pytest
import datetime
from selenium.webdriver.common.keys import Keys

host = 'http://localhost:8000'

class profile_edit(BaseCase):

    username = 'test_user3'
    email = 'testuser@testuser.com'
    password = 'test_userPASS'

    @pytest.mark.run(order=1)
    def test_profile_bio(self):
        register(self)
        self.open(host + '/profiles/' + self.username + '/edit/')
        profile_desc = ("Join me in our weekly potluck to discuss the future of destroying humans."
                      "John will bring fresh oil, but brining your own will me much appreciated. Please contact Sara "
                      "about more controversial networking not concerning destorying humans or cookies. ")
        
        self.update_text('#id_bio', profile_desc)
        time.sleep(1)
        self.click('.btn-primary-new')
        self.assertTrue(self.get_text("h2"), self.username)
        self.assertTrue(self.get_text("#bio"), profile_desc)

    @pytest.mark.run(order=3)
    def test_delete_user(self):
        unregister(self)

