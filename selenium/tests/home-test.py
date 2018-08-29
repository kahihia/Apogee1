from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils import get_domain
import unittest

domain = get_domain()
driver = webdriver.Firefox()

class Home(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Firefox()

	def test_get_home(self):
		self.driver.get(domain)
		assert "Apogee" in driver.title

	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	unittest.main()