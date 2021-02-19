# Unit testing Flask

## Identifying the test cases

Last week we created login functionality and at the end of the activity suggests a number of tests that could be carried
out:

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

It might seem tedious to write the tests like this, and you do not have to do so, however you as you are getting started
with testing you might find it helps you to think about:

- anything you might need to set-up for your tests (e.g. setup)
- assertions that may be appropriate for your tests
- edge cases and error cases

It should also help you to work out the steps needed for each test.

## Pytest or unittest?

Pytest supports execution of unittest test cases, with additional features that purport to make it easier to write test
cases. There are also helper libraries such as pytest-flask.
The [official Flask tutorial](https://flask.palletsprojects.com/en/1.1.x/testing/) uses pytest.

Unittest is provided with python. There are also helper libraries such as Flask-Testing that extend unittest for working
with Flask apps. Students from this course last year reported that they found Flask-Testing easy to use.

You may choose either for the coursework.

Selenium webdriver, which we will use in a later activity, works with both pytest and unittest.

Most of the activities in this course use pytest since this is what was used in COMP0035.

## Configure testing for the project in your IDE

You will need to install the following (these are in requirements.txt).

```text
pytest
selenium
```

You may also need to configure your IDE to use pytest to run the tests. For
PyCharm [enable pytest for the project](https://www.jetbrains.com/help/pycharm/pytest.html#enable-pytest).

## Check your TestConfig parameters

Consider checking or modifying the following parameters in your `config.py`:

```python
class TestConfig(Config):
    TESTING = True
    #  You may wish to use an memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    #  Echo SQL to the console, useful for debugging database queries
    SQLALCHEMY_ECHO = True
    #  Allow forms to be submitted from the tests without the CSRF token
    WTF_CSRF_ENABLED = False
```

## Create a test directory

The [Pytest documentation discusses](https://docs.pytest.org/en/stable/goodpractices.html#choosing-a-test-layout-import-rules)
in some detail the options for structuring tests into directories.

Create a Python package in the project called `tests` in the project directory.

Most tools don’t require a specific location, however typically you will add a directory called ‘tests’ at the same
level as your app folder.

Name your test files using the format `test_*.py` e.g. `test_users.py`. Many test tools will automatically discover
tests if they are named according to a given convention.

Name each test function within your `test_*.py` s.g. `def test_empty_db:`. Most test tools will identify tests to run if
they follow a given naming convention.

Refer to COMP0035 for more information on naming conventions for tests.

## Basic anatomy of a test file

A [classic x-unit structure](https://docs.pytest.org/en/latest/xunit_setup.html) has:

- **Setup method**: set up initial state for each, or all, test methods
- **Teardown method**: perform clean-up after each, or all, test method completes
- **Test methods**: perform the individual tests

Setup/teardown can be applied to module, function, class or method level.

Setup/teardown are collectively referred to as fixtures (a test fixture is something used to consistently test a piece
of software).

The Flask-Testing library also requires that you provide an implementation for `create_app()`. This is not the same as
the `create_app()` function you created for the Flask app (e.g. in `__init__.py` for the app module). However, you can
call your existing `create_app()` in the TestCase create_app() method (as is shown in the following code).

The following shows an example of a basic test file structure, including the create_app() method, using unittest:

```python
from unittest import TestCase
from my_app import create_app, db
from my_app.config import TestingConfig


class BaseTest(TestCase):
    def create_app(self):
        app = create_app(TestingConfig)
        return app

    def setUp(self):
        db.create_all()
        self.mock_data = [1, 2, 3, 4, 5]

    def tearDown(self):
        self.mock_data = []
        db.drop_all()

    def someTest(self):
        self.assertEqual(len(self.mock_data), 5)

```

## Fixtures in pytest

Pytest provides a fixture decorator, [`@pytest.fixture`](https://docs.pytest.org/en/latest/fixture.html), that can be
used instead of setup/teardown to provide resources for the tests.

Fixture objects are defined and then passed as needed into test functions, methods and classes as input arguments (i.e.
only use the fixtures you need for a given test).

This activity only provides an overview of the use of fixtures, refer to
the [API documentation](https://docs.pytest.org/en/latest/fixture.html) for further features and examples.

Pytest fixtures can be defined for a scope:

- `function` Run once per test
- `class` Run once per class of tests
- `module` Run once per module
- `session` Run once per session

A fixture is a python method with the fixture decorator. There are also a couple of other points to note. Typically you
will `yield` a resource rather than using `return`; secondly you can use a `finaliser` which provides the teardown.

For example:

```python
import smtplib
import pytest


@pytest.fixture(scope="module")
def smtp_conn(request):
    smtp_conn = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    yield smtp_conn  # provide the fixture value

    def fin():
        smtp_conn.close()

    request.addfinalizer(fin)  # tear down 

```

Creating a `conftest.py` allows you to share fixtures across multiple files.

The conftest.py file serves as a means of providing fixtures for an entire directory.

Fixtures defined in a conftest.py can be used by any test in that package without needing to import them (pytest will
automatically discover them).

You can have multiple nested directories/packages containing your tests, and each directory can have its own conftest.py
with its own fixtures, adding on to the ones provided by the conftest.py files in parent directories.

## Create a `conftest.py`

Create a python file called `conftest.py` in the test directory.

Add a fixture to provide the test Flask app:

```python
import pytest
from my_app import create_app
from my_app.config import TestingConfig


@pytest.fixture(scope='session')
def app(request):
    """ Returns a session wide Flask app """
    _app = create_app(TestingConfig)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()
```

“Flask provides a way to test your application by exposing
the [Werkzeug test Client](https://werkzeug.palletsprojects.com/en/1.0.x/test/) and handling the context locals for you.
You can then use that test client with your favourite testing solution.”

You use the test client with both unittest and pytest.

The next fixture to add is the test client:

```python
import pytest


@pytest.fixture(scope='session')
def client(app):
    """ Exposes the Werkzeug test client for use in the tests. """
    return app.test_client()
```

Since we also need to be able to use the SQLAlchemy database then we need two further fixtures:

1. To provide and initialise the database with the area table added.
2. To handles rolling back transactions between each test. This test has function scope (i.e. per test).

```python
import pytest
import pandas as pd
from my_app import db as _db


@pytest.fixture(scope='session')
def db(app):
    """
    Returns a session wide database using a Flask-SQLAlchemy database connection.
    """
    _db.app = app
    _db.create_all()
    # Add the local authority data to the database (this is a workaround you don't need this for your coursework!)
    csv_file = Path(__file__).parent.parent.joinpath("data/household_recycling.csv")
    df = pd.read_csv(csv_file, usecols=['Code', 'Area'])
    df.drop_duplicates(inplace=True)
    df.set_index('Code', inplace=True)
    df.to_sql('area', _db.engine, if_exists='replace')

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    """ Rolls back database changes at the end of each test """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()
```

For many of the tests we need to create a test User so let's provide one as a fixture so it can be used in multiple
tests.

```python
import pytest


@pytest.fixture(scope='function')
def user(db):
    """ Creates a user without a profile. """
    from my_app.models import User
    user = User(firstname="Person", lastname='One', email='person1@people.com')
    user.set_password('password1')
    db.session.add(user)
    db.session.commit()
    return user

```

## Write the tests

We have already specified the tests using the GIVEN, WHEN, THEN which should help you consider how to structure the
tests and define the assertions.

'GIVEN' suggests any preparation that is needed, e.g. such as creating a test user
'WHEN' suggests the action to carry out with the client
'THEN' suggests the assertion

Look at this example:

```python
def test_index_page_valid(client):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200
```

GIVEN requires the Flask app which will be created for us by the app fixture so we don't need to do anything further for
this test.

WHEN says that we need to go to the home page which is done using `client.get('/')`

When you submit a request to a url using the test client it returns a response. The response contains attributes that
you can check for in your assertions.

For example, `response.status_code` will tell you the status code that was
returned. [List of HTTP codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

`response.data` gives you the HTML content so you can check for any content you would expect in the HTML such as the
value of a particular tag. To match strings from the response data you need to use the binary syntax
e.g. `assert b'some string' in response.data`

We want to test the result of going to the home page so we really need `response = client.get('/')`

THEN is the assertion which in this case checks that in the response the status code is 200.

## Write tests

Create a python file with an appropriate name, e.g. it should start with `test_` and be in the `tests` directory.

Try and write a test for each of the tests we specified at the start of this document.

Below are some tests that should work if you want to refer to them for examples of how to carry out a test.

## Some examples tests

```python
from my_app.models import User


def test_profile_not_allowed_when_user_not_logged_in(client):
    """
    GIVEN A user is not logged
    WHEN When they access the profile menu option
    THEN they should be redirected to the login page
    """
    response = client.get('/community/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data


def test_signup_succeeds(client):
    """
        GIVEN A user is not registered
        WHEN When they submit a valid registration form
        THEN they the should be redirected to a page with a custom welcome message and there should be an additional
        record in the user table in the database
    """
    count = User.query.count()
    response = client.post('/signup', data=dict(
        first_name='Person',
        last_name='Two',
        email='person_2@people.com',
        password='password2',
        password_repeat='password2'
    ), follow_redirects=True)
    count2 = User.query.count()
    assert count2 - count == 1
    assert response.status_code == 200
    assert b'Person' in response.data
```