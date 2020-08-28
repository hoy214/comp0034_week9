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
When using pytest we can define the fixture functions in a file called `conftest.py`. This makes them accessible across multiple test files.

The first fixture is required and provides the test Flask app:

```python
import pytest
from my_app import create_app, config

@pytest.yield_fixture(scope='session')
def app(request):
    """ Returns a session wide Flask app """
    _app = create_app(config.TestConfig)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()
```

The next fixture to add is the test client:
```python
import pytest


@pytest.fixture(scope='session')
def client(app):
    """ Exposes the Werkzeug test client for use in the tests. """
    return app.test_client()
```

Since we also need to be able to use the SQLAlchemy database then we need two further fixtures: 
1. To provide and initialise the database with the country data added.
2. To handles rolling back transactions between each test. This test has function scope (i.e. per test).

```python
import pytest
from my_app import add_countries
from my_app import db as _db


@pytest.yield_fixture(scope='session')
def db(app):
    """
    Returns a session wide database using a Flask-SQLAlchemy database connection.
    Country list is added to the database.
    """
    _db.app = app
    _db.create_all()
    add_countries(app)
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

For many of the tests we need to create a test User so let's provide one as a fixture so it can be used in multiple tests.
```python
import pytest


@pytest.fixture(scope='function')
def user(db):
    """ Creates a user without a profile. """
    from my_app.models import User
    user = User(firsname="Person", lastname='One', email='person1@people.com')
    user.set_password('password1')
    db.session.add(user)
    db.session.commit()
    return user

```

## Write the tests
We have already specified the tests using the GIVEN, WHEN, THEN which should help you consider how to structure the tests and define the assertions.

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

GIVEN requires the Flask app which will be created for us by the app fixture so we don't need to do anything further for this test.

WHEN says that we need to go to the home page which is done using `client.get('/')`

When you submit a request to a url using the test client it returns a response. The response contains attributes that you can check for in your assertions.

For example, `response.status_code` will tell you the status code that was returned. [List of HTTP codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

`response.data` gives you the HTML content so you can check for any content you would expect in the HTML such as the value of a particular tag. To match strings from the response data you need to use the binary syntax e.g. `assert b'some string' in response.data`

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
        first_name='First',
        last_name='Last',
        email='email@address.com',
        password='password',
        password_repeat='password'
    ), follow_redirects=True)
    count2 = User.query.count()
    assert count2 - count == 1
    assert response.status_code == 200
    assert b'First' in response.data
```