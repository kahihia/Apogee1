from seleniumbase import BaseCase
import time
from login import login, fan_login
from registration import register, unregister, fan_register, fan_unregister

import pytest
import datetime
from selenium.webdriver.common.keys import Keys

host = 'http://localhost:8000'

class create_fparty(BaseCase):

    username = 'test_user3'
    email = 'testuser@testuser.com'
    password = 'test_userPASS'

    fan_username = 'test_fan'
    fan_email = 'testfan@testfan.com'
    fan_password = 'test_fan'

    cur_event_link = None

    @pytest.mark.run(order=1)
    def test_create_buy(self):
        # Create as a Creator
        register(self)
        event_title = "DESTROY ALL HUMANS"
        possible_winners = '10'
        cost = '10.00'
        event_desc = ("Join me in our weekly potluck to discuss the future of destroying humans."
                      "John will bring fresh oil, but brining your own will me much appreciated. Please contact Sara "
                      "about more controversial networking not concerning destorying humans. ")
        self.open(host + '/events/create/')
        self.update_text('#id_title', event_title)
        self.update_text('#id_description', event_desc)
        self.update_text('#id_datetime', datetime.date(2022, 11, 9).strftime('%Y-%m-%d %H:%M'))
        self.find_element("#id_event_type").send_keys(3)
        self.find_element("#id_event_type").send_keys(Keys.UP)
        self.find_element("#id_event_type").send_keys(Keys.DOWN)
        self.find_element("#id_event_type").send_keys(Keys.DOWN)
        self.update_text("#id_num_possible_winners", possible_winners)
        self.update_text("#id_cost", cost)
        time.sleep(10)
        self.click('.btn-primary-new')
        self.assertTrue(self.get_text("h1"), event_title)
        self.assertTrue(self.get_text("#num_curr_winners"), '0')
        self.assertTrue(self.get_text("#num_possible_winners"), possible_winners)
        cur_event_link = self.get_current_url()
        self.open(host + '/accounts/logout/')
        # Join as a User
        fan_login(self)
        self.open(cur_event_link)
        self.assertTrue(self.get_text("h1"), "DESTROY ALL HUMANS")
        self.assertTrue(self.get_text(".joinBtn"), "Join")
        self.click(".joinBtn")
        time.sleep(3)
        self.assertTrue(self.get_text(".joinBtn"), "Joined")
        self.open(host + '/accounts/logout/')

    @pytest.mark.run(order=3)
    def test_create_lottery(self):
        login(self)
        event_title = "DESTROY ALL HUMANS"
        possible_winners = '10'
        cost = '10.00'
        max_entrants = '25'
        event_desc = ("Join me in our weekly potluck to discuss the future of destroying humans."
                      "John will bring fresh oil, but brining your own will me much appreciated. Please contact Sara "
                      "about more controversial networking not concerning destorying humans. ")
        self.open(host + '/events/create/')
        self.update_text('#id_title', event_title)
        self.update_text('#id_description', event_desc)
        self.update_text('#id_datetime', datetime.date(2022, 11, 9).strftime('%Y-%m-%d %H:%M'))
        self.find_element("#id_max_entrants").send_keys(3)
        self.find_element("#id_max_entrants").send_keys(Keys.UP)
        self.find_element("#id_max_entrants").send_keys(Keys.DOWN)
        self.find_element("#id_max_entrants").send_keys(Keys.DOWN)
        self.find_element("#id_max_entrants").send_keys(Keys.DOWN)
        self.update_text("#id_num_possible_winners", possible_winners)
        self.update_text("#id_cost", cost)
        time.sleep(10)
        self.click('.btn-primary-new')
        self.assertTrue(self.get_text("h1"), event_title)
        self.assertTrue(self.get_text("#num_joined"), "0")
        self.assertTrue(self.get_text("#max_entrants"), max_entrants)
        self.assertTrue(self.get_text("#num_possible_winners"), possible_winners)
        cur_event_link = self.get_current_url()
        self.open(host + '/accounts/logout/')
        # Join as a User
        fan_login(self)
        self.open(cur_event_link)
        self.assertTrue(self.get_text("h1"), "DESTROY ALL HUMANS")
        self.assertTrue(self.get_text(".joinBtn"), "Join")
        self.click(".joinBtn")
        time.sleep(3)
        self.assertTrue(self.get_text(".joinBtn"), "Joined")
        self.open(host + '/accounts/logout/')

    @pytest.mark.run(order=5)
    def test_create_bid(self):
        # Create as a Creator
        login(self)
        event_title = "DESTROY ALL HUMANS"
        possible_winners = '10'
        cost = '10.00'
        event_desc = ("Join me in our weekly potluck to discuss the future of destroying humans."
                      "John will bring fresh oil, but brining your own will me much appreciated. Please contact Sara "
                      "about more controversial networking not concerning destorying humans. ")
        self.open(host + '/events/create/')
        self.update_text('#id_title', event_title)
        self.update_text('#id_description', event_desc)
        self.update_text('#id_datetime', datetime.date(2022, 11, 9).strftime('%Y-%m-%d %H:%M'))
        self.find_element("#id_event_type").send_keys(3)
        self.find_element("#id_event_type").send_keys(Keys.UP)
        self.find_element("#id_event_type").send_keys(Keys.DOWN)
        self.update_text("#id_num_possible_winners", possible_winners)
        self.update_text("#id_cost", cost)
        time.sleep(10)
        self.click('.btn-primary-new')
        self.assertTrue(self.get_text("h1"), event_title)
        self.assertTrue(self.get_text("#num_possible_winners"), possible_winners)
        cur_event_link = self.get_current_url()
        self.open(host + '/accounts/logout/')
        # Join as a User
        fan_login(self)
        self.open(cur_event_link)
        self.assertTrue(self.get_text("h1"), "DESTROY ALL HUMANS")
        self.assertTrue(self.get_text(".joinBtn"), "Join")
        self.update_text("#bid_amount", "10.50")
        self.click(".joinBtn")
        time.sleep(3)
        self.assertTrue(self.get_text(".joinBtn"), "Joined")
        self.open(host + '/accounts/logout/')

    @pytest.mark.run(order=6)
    def test_delete_creator(self):
        unregister(self)