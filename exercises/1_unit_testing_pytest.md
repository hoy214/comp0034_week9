# Unit tests with pytest

In week 6 (exercise 3 in week 6 GitHub) we established login and at the end of the activity suggests a number of tests that could be carried out:
- Sign up a new user
- Try to login with an incorrect email address (error message should be displayed on the form)
- Try to login with an incorrect password (error message should be displayed on the form)
- Logon with correct details and tick remember me
- Close the browser and reopen within a minute, you should still be logged in (logout shows in the navbar)
- Close the browser and wait longer than a minute, you should be logged out (login shows in the navbar)
- Choose Logout from the navbar, you should be logged out (login shows in the navbar)

We will use these as the basis for this activity.

We will first write the tests using the GIVEN, WHEN, THEN model:
```text
GIVEN a User model
WHEN a new User is created
THEN check the email, hashed_password, authenticated, and role fields are defined correctly
```

So the above few tests might read like this:
```text
GIVEN a User has been created
WHEN the user logs in with the wrong email address
THEN then an error message should be displayed on the login form ('No account found with that email address.')

GIVEN a User has been created
WHEN the user logs in with the wrong password
THEN then an error message should be displayed on the login form ('Incorrect password.')

GIVEN a User is logged in and selected Remember Me
WHEN they close the browser and re-open it within 60 seconds
THEN they should remain logged in

GIVEN a User is logged in and selected Remember Me
WHEN they close the browser and re-open after 60 seconds
THEN they should be required to login again to access any protected pages (such as community home)

GIVEN a User logged out
WHEN they access the navigation bar
THEN there should be an option to login in
```

Try and specify a few more tests. If you can't think of any consider the profile functionality and write tests for:
1. What you would expect to happen when a User does not have a profile and they select the profile menu option.
2. What you would expect to happen when a User tries to add a profile with the same username as another user.

```text
GIVEN
WHEN
THEN

GIVEN
WHEN
THEN

```

It might seem tedious to write the tests like this, and you do not have to do so, however you as you are getting started with testing you might find it helps you to think about:
- anything you might need to set-up for your tests (e.g. setup)
- assertions that may be appropriate for your tests
- edge cases and error cases

It should also help you to work out the steps needed for each test.

## Configure testing for the project in your IDE
You will need to install the following (these are in requirements.txt)
```text
pytest
selenium
```

You may also need to configure your IDE to use pytest to run the tests. 
For PyCharm [enable pytest for the project](https://www.jetbrains.com/help/pycharm/pytest.html#enable-pytest).

Create a Python package in the project called `tests`.

## conftest.py
Pytest We can define the fixture functions in this file to make them accessible across multiple test files.

```python
class MyTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
```
