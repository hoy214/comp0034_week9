# Front end testing with Selenium Webdriver

## Selenium webdriver

### Overview

The Flask test client cannot fully emulate the environment of a running application. For example, an application that
relies on JavaScript code running in the client browser will not work, as the JavaScript code included in the responses
will be returned to the test without being executed. The behaviour of the application may also vary in different
browsers.

The selenium webdriver API allows you to programmatically interact with a browser the way a real user would and is most
commonly used for testing. Support is provided for most programming languages. It does not have a built-in framework for
actually running tests (relies on provided tools, e.g. unittest).

### Getting started

You need to install the correct driver for your browser and operating system. This is explained below and in more detail
in the [Getting Started documentation](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/) on the
Selenium website.

### Targeting elements

Selenium works
by [targeting elements](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/locating_elements/) on
a web page. You will need to identify elements on the page to target e.g.

```python
driver.find_element(By.ID, "cheese")
cheese = driver.find_element(By.ID, "cheese")
cheddar = cheese.find_elements_by_id("cheddar")
cheddar = driver.find_element_by_css_selector("#cheese #cheddar")
mucho_cheese = driver.find_elements_by_css_selector("#cheese li")  # Finds a list of elements
driver.find_element_by_css_selector("#role")
```

There are eight different built-in element location strategies in WebDriver:

1. `class name` Locates elements whose class name contains the search value (compound class names are not permitted).
2. `css selector` Locates elements matching a CSS selector.
3. `id` Locates elements whose ID attribute matches the search value.
4. `name` Locates elements whose NAME attribute matches the search value.
5. `link text` Locates anchor elements whose visible text matches the search value.
6. `partial link text` Locates anchor elements whose visible text contains the search value. If multiple elements are
   matching, only the first one will be selected.
7. `tag name` Locates elements whose tag name matches the search value
8. `xpath` Locates elements matching an XPath expression

The recommended approach is to use `id` wherever possible as this avoids more complex DOM traversals.

### Passing text values to an element

If you want to complete a form, then you can pass values to complete an element e.g. to add the name Charles to the name
input of a form:

```python
name = 'Charles'
driver.find_element_by_name("name").send_keys(name)
```

You can then submit a form using the click method e.g.

```python
driver.find_element_by_css_selector("input[type='submit']").click()
```

### Waits

It is possible that a test executes faster than the browser responds, you may therefore need to include
explicit [waits](https://www.selenium.dev/documentation/en/webdriver/waits/) e.g. to wait until a particular element is
loaded before trying to locate it in the test. You can wait for any of
the [expected conditions listed in the documentation](https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html?highlight=expected)
.

```python
WebDriverWait(driver, timeout=3).until(some_condition)
```

Or wait for a specific period of time:

```python
driver.implicitly_wait(10)
```

### Assertions

The Selenium Webdriver API relies on a testing library for the test capability. You therefore use the assertions for the
testing library you choose e.g. pytest or unittest.

### A few examples from the documentation

Once you have navigated to a given URL using the driver then you can select web elements as follows:

```python
# Get search box element from webElement 'q' using Find Element
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("webdriver")

# Get all the elements available with tag name 'p'
elements = driver.find_elements(By.TAG_NAME, 'p')
for e in elements:
    print(e.text)

# Find element from element
search_form = driver.find_element(By.TAG_NAME, "form")
search_box = search_form.find_element(By.NAME, "q")
search_box.send_keys("webdriver")

# Get element with tag name 'div'
element = driver.find_element(By.TAG_NAME, 'div')

# Get all the elements available with tag name 'p'
elements = element.find_elements(By.TAG_NAME, 'p')
for e in elements:
    print(e.text)

# Get attribute of current active element
attr = driver.switch_to.active_element.get_attribute("title")
print(attr)

# Returns true if element is enabled else returns false
value = driver.find_element(By.NAME, 'btnK').is_enabled()

# Returns true if element is checked else returns false
value = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']:first-of-type").is_selected()

# Returns TagName of the element
attr = driver.find_element(By.CSS_SELECTOR, "h1").tag_name

# Returns height, width, x and y coordinates referenced element
res = driver.find_element(By.CSS_SELECTOR, "h1").rect

# Retrieves the computed style property 'color' of linktext
cssValue = driver.findElement(By.LINK_TEXT, "More information...").value_of_css_property('color')

# Retrieves the text of the element
text = driver.find_element(By.CSS_SELECTOR, "h1").text
```

## Download and install the correct version of Chrome driver for your computer

You have already used Selenium Webdriver in week 5 for the Dash app testing activity then skip this step.

Check your version of Chrome in the Chrome settings.

For example, mine is: Version 84.0.4147.125.

![chrome settings](img/chrome_settings.png)

Go to [Chrome driver downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads) and select the version
for your version Chrome.

In the next window you then need to download the correct driver for your operating system.

The [Selenium documentation](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/) explains where to
place it in Windows and how to add it to the path, and for MacOS.

My experience on a MacBook was that I also had to complete the following steps:

- Download the driver
- Try to open the driver from the download directory, this prompts you to change the security settings for the file (
  System Settings | Security & Privacy | General and then click on 'Open Anyway').
- Close the driver
- Move the driver from downloads to usr/local/bin

## Create test fixtures to support selenium

The first fixture creates a ChromeDriver with options that are required for running in a CI environment. You will need
these if you plan to use This only tests in Chrome, you will need to investigate the documentation if you also wish to
test with other supported browsers.

The second fixure runs the Flask app in a thread. There is very little documentation explaining how to use Flask with
Selenium and Unittest. You may wish to investigate flask-testing and use its `live_server` decorator rather than the
following as it is supported and has better error handling.

If you wish to use unittest rather than pytest then Flask-Testing is well supported by examples and documentation.

```python
@pytest.fixture(scope='class')
def chrome_driver(request):
    """ Fixture for selenium webdriver with options to support running in GitHub actions"""
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    chrome_driver = webdriver.Chrome(options=options)
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()


@pytest.fixture(scope='class')
def selenium(app):
    """
    Fixture to run the Flask app
    A better alternative would be to use flask-testing live_server
    """
    process = multiprocessing.Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()
```

## Create a new test file and test class

Create a new test file e.g. `test_my_app_browser.py`. 

Create a new test class within it and add a test that the home page is available e.g.:

```python
class TestMyAppBrowser:
    def test_app_is_running(self, app):
        self.driver.get("http://127.0.0.1:5000/")
        assert self.driver.title == 'Home page'
```

Add a test to test the signup process is successful e.g.:
```python

```

## Over to you
Try to create at least one more test e.g.

- test creating a profile with username and bio succeeds
- test login fails if an incorrect password is entered