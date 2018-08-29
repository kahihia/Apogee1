# Selenium Browser Test

### Install 
From the source - https://selenium-python.readthedocs.io/installation.html#introduction

First you'll need the Java runtime enviorment http://www.oracle.com/technetwork/java/javase/downloads/index.html
Then the python selenium package
The core selenium package in included in this repo

`pip install selenium`

Verify everything is working with 
`python test.py`

### Running Tests

To run a single test
`python ./tests/home-test.py`

To run a single test in a different enviorment add the full protol and domain that you wish to test
`python ./tests/home-test.py https://dev.apogee.gg/`

To run the suite of tests using multiple browsers
`python ./run_test_suite.sh`

### To Add New Tests

Create a file in ./tests that ends in \*-test.py, the test suite runner will run all of these names when run
`touch ./tests/*name*-test.py`

Create a basic scafold for the test using unittest

```
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
```

Setup is called to start the browser when a new unit test is created, and teardown is called to close it at the end of the unit test
For more selenium commands go to https://selenium-python.readthedocs.io/getting-started.html