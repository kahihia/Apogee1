# Selenium Tests
The tests in this folder are meant to end-to-end test the application. Make sure you have pytest in your enviorment and then you can run tests with the command pytest *mytest*.py. Make sure to have the application running on localhost:8000 for the tests to work or change the host variable in the test you want to run to point to the enviorment you would like to test. TODO: make that a command line argument

### Installation
Tests run on the python package Selenium Base, as its not available via pip it is included in the repo as a git submodule. If you don't see a SeleniumBase directory under selenium tests run the below command to install it. You may also need to install the latest version of JAVA.

`git submodule update --init --recursive`

For more information on the selenium api Selenium Base that is included in this project visit http://seleniumbase.com/

### Important Notes
**create_party.py** - currently while the test if running during the create stage, you must submit a picture for the test to use, it will allow you a 10 second delay to do so
**fanside_events.py** - to be able to test joining events, you must first add funds to the test fan account you can do this by the following

```
Create user with the following attributes:
------------------------------------------
fan_username = 'test_fan'
fan_email = 'testfan@testfan.com'
fan_password = 'test_fan'

Then either add funds via the funds page or via postgres if your enviorment is not linked with paypal like so

psql apogeetestdb
UPDATE accounts_userprofile SET account_balance = 200 WHERE id =  (SELECT id FROM auth_user WHERE username='test_fan');


```

### What Needs To Be Tested Manually
* Paypal payments
* Blocked Users - on testing backlog
* Transfer of funds between fans and creators - more efficient via unit testing but here to double check
* Payout
* Notifications
* Anything Celery Based