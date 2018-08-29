from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

if len(sys.argv) > 1:
	 domain = "https://" + sys.argv[2]
else:
	 domain = "http://localhost:8000"

print("Domain to test: " + domain)

def gets_homepage():
	driver = webdriver.Firefox()
	driver.get(domain)
	assert "Apogee" in driver.title