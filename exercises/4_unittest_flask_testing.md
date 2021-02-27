# Testing with unittest, Flask-Testing and GitHubActions

## Purpose of this activity

This is an additional activity created for the groups that prefer to use unittest and Flask-Testing.

This supplements activities 1, 2 and 3 with specific additional guidance for applying the learning from those activities to testing
with unittest rather than pytest. 

Following this exercise without the previous exercises won't be sufficient.

## Unit testing differences

### Installation and set-up

Unittest is installed with Python so you don't need to explicitly install it.

For students using PyCharm, go to the Settings/Preferences and go to Tools > Python Integrated Tools and change the
default test runner to be unittest.

You will need to install [Flask-Testing](https://flask-testing.readthedocs.io/en/latest/) e.g. `pip install Flask-Testing`or in PyCharm you can add it from Settings/Preferences > Project > Python Interpreter.

### Basic test structure

The following is from the [unittest documentation](https://docs.python.org/3/library/unittest.html):

```python
import unittest


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
```

#### Fixtures

Unittest uses methods for creating fixtures for [setup and teardown](https://docs.python.org/3/library/unittest.html#unittest.TestCase).

Flask-Testing supports `setUp` and `tearDown` and provides an additional method `create_all` to create a Flask test client app.

Create a BaseTestCase that inherits from Flask-Testing TestCase and LiveServerTestCase e.g.

```python
import requests
from my_app import db, config, create_app
from flask_testing import TestCase, LiveServerTestCase


class BaseTestCase(TestCase):
    """Base test case."""
    def create_app(self):
        app = create_app(config.TestingConfig)
        return app

    def test_server_is_up_and_running(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)
        
    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

```

You can also create other fixtures as methods e.g.

```python
from flask_testing import TestCase, LiveServerTestCase

class BaseTestCase(TestCase, LiveServerTestCase):
    # create_app, setup & teardown ommited

    def login(self, email, password):
        return self.client.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.client.get(
            '/logout',
            follow_redirects=True
        )

```

### Assertions

Whereas pytest uses 'assert', unittest uses a range of different assertions [listed in the API test class documentation](https://docs.python.org/3/library/unittest.html#unittest.TestCase) e.g.

```text
assertEqual
assertNotEqual
assertTrue
assertFalse
assertRaises
AssertWarns
assertRaisesRegex
assertIsAlmostEqual
assertIsNotAlmostEqual
assertGreaterEqual
assertGreater
assertLess
assertLessEqual
assertRound
assertNotRound
assertIs
assertNotIs
assertNot

...and more

```

### Coverage

If not already installed then install [coverage](https://coverage.readthedocs.io/en/coverage-5.4/).

The documentation explains how to run unittest tests from the command line.

To run it in PyCharm, right click on the test or the tests directory in the Project pane and select to 'Run unittest
with Coverage'.

## Testing with Selenium ChromeDriver
To test with Flask-Testing and Selenium ChromeDriver you can configure the driver in the base case e.g.:

```python
import requests
from flask_testing import LiveServerTestCase
from selenium import webdriver

from my_app import db, create_app, config

class TestBase(LiveServerTestCase):
    """
    Base test class for the selenium tests
    """

    def create_app(self):
        app = create_app(config.TestingConfig)
        app.config['LIVESERVER_PORT'] = 0
        return app

    def setUp(self):
        """ Creates the chrome driver and adds tables to the database plus the country data """
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

    def tearDown(self):
        """ Quit the webriver and drop tables from database """
        db.drop_all()
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)
```

The tests themselves will be the similar to those for pytest except that you inherit the TestBase class e.g.:

```python
class TestRegistration(TestBase):

    def test_registration_succeeds(self):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly, and that
        they will be redirected to the index page
        """

        # Click signup menu link
        self.driver.find_element_by_id("signup-nav").click()
        self.driver.implicitly_wait(10)

        # Test person data
        first_name = "First"
        last_name = "Last"
        email = "email@ucl.ac.uk"
        password = "password1"
        password_repeat = "password1"

        # Fill in registration form
        self.driver.find_element_by_id("first_name").send_keys(first_name)
        self.driver.find_element_by_id("last_name").send_keys(last_name)
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("password_repeat").send_keys(password_repeat)
        self.driver.find_element_by_id("submit").click()
        self.driver.implicitly_wait(10)

        # Assert that browser redirects to index page
        self.assertIn(url_for('main.index'), self.driver.current_url)

        # Assert success message is flashed on the index page
        message = self.driver.find_element_by_id("messages").find_element_by_tag_name("li").text
        self.assertIn(f"Hello, {first_name} {last_name}. You are signed up.", message)
```

## GitHub actions
See exercise 4 for how to set-up GitHub actions.

You will need the following .yml instead of that shown in the original exercise:

```yaml
name: Flask app CI and Lint

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 coverage
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with unittest and coverage        
      run: |
        coverage run -m --source=my_app unittest discover tests_unittest
        coverage report
```