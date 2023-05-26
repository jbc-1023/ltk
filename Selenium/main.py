import os
import time
import random
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from english_words import get_english_words_set
from PIL import Image
import numpy as np

""" --------------------------------------------------------------------------
Expected categories 
----------------------------------------------------------------------------"""


categories_test_data_map = [
    ["category-item/category-ltkfind", "LTK Find"],
    ["category-item/category-seasonal", "Summer Trends"],
    ["category-item/category-ltku", "LTK-U"],
    ["category-item/category-home", "Home"],
    ["category-item/category-salealert", "Deal Alert"],
    ["category-item/category-under50", "Under $50"],
    ["category-item/category-under100", "Under $100"],
    ["category-item/category-styletip", "Style Tips"],
    ["category-item/category-beauty", "Beauty"],
    ["category-item/category-fit", "Fitness"],
    ["category-item/category-curves", "Curves"],
    ["category-item/category-video", "Shoppable Video"],
    ["category-item/category-workwear", "Workwear"],
    ["category-item/category-swim", "Swim"],
    ["category-item/category-travel", "Travel"],
    ["category-item/category-shoecrush", "Shoe Crushes"],
    ["category-item/category-itbag", "It Bags"],
    ["category-item/category-baby", "Baby"],
    ["category-item/category-bump", "Bump"],
    ["category-item/category-kids", "Kids"],
    ["category-item/category-family", "Family"],
    ["category-item/category-mens", "Mens"],
    ["category-item/category-wedding", "Weddings"],
    ["category-item/category-europe", "Europe"],
    ["category-item/category-brasil", "Brasil"]
]


""" --------------------------------------------------------------------------
Helper functions 
----------------------------------------------------------------------------"""


def verify_landing(b):
    # Verify landed on home page
    retry_max = 20  # Max number of retries
    retry = 1  # Number of times to retry (seconds)
    page_found = False  # Flag for when page is found
    landing_page = "https://www.shopltk.com/home/for-you"  # The expected page
    while retry <= retry_max:
        if b.current_url == landing_page:
            page_found = True
            break
        else:
            if retry > retry_max*.66:
                print(f"Retry {retry}/{retry_max}")
            time.sleep(1)
            retry += 1
    assert page_found, f"Did not land on expected page {landing_page}"
    """
    Can change this to a softer fail so that test will not stop if one Browser fails
    """


def browser_setup(browser="Chrome", headless=False):
    """
    Setup a browser and returns the driver of that browser
    """
    try:
        if browser == "Chrome":
            if headless:    # Turn on headless if specified
                op = Options()
                op.add_argument("--headless")
                b = webdriver.Chrome(options=op)
            else:
                b = webdriver.Chrome()
        elif browser == "Firefox":
            if headless:   # Turn on headless if specified
                op = Options()
                op.add_argument("--headless")
                b = webdriver.Firefox(options=op)
            else:
                b = webdriver.Firefox()
        elif browser == "Safari":
            if headless:   # Turn on headless if specified
                op = Options()
                op.add_argument("-browser")
                b = webdriver.Safari(technology_preview=True, options=op)
                b.set_window_size(100, 100)
            else:
                b = webdriver.Safari()
        else:
            print(f"The browser {browser} is not supported")
            exit(1)
        return b
    except:
        print(f"Problem trying to open browser {browser}. Browser not installed or wrong OS?")
        exit(1)


def generate_word(min_length=1, max_length=10):
    """
    Generate a random real English word
    """
    words_set = get_english_words_set(['web2'], lower=True)
    out_word = random.choice(list(words_set))
    while (len(out_word) > max_length) or (len(out_word) < min_length):
        out_word = random.choice(list(words_set))
    return out_word


def random_email():
    """
    Generate a random email
    Using my real personal email to preserve "email reputation" to avoid spam flagging
    """
    return 'joshuabchu+'+generate_word()+'_'+generate_word()+'@gmail.com'


def login(b, login_email, login_password):
    # Go to webpage
    b.get("https://www.shopltk.com")
    time.sleep(3)

    # Login with username and password
    b.find_element(By.XPATH, "//span[contains(text(), 'Log in')]").click()
    time.sleep(3)
    b.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(login_email)
    time.sleep(1)
    b.find_element(By.CSS_SELECTOR, "button[type='submit").click()
    time.sleep(1)
    b.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(login_password)
    b.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(Keys.RETURN)

    # Verify landed on home page
    verify_landing(b)
    time.sleep(3)


def UI_automation(browser):
    """
    UI Automation

    1) Go to www.shopltk.com
    2) Register
    3) Verify landing page
    """

    # Get browser
    b = browser_setup(browser)

    # Go to web page
    b.get("https://www.shopltk.com")
    time.sleep(3)
    """
    NOTE: Using time.sleep(2) for now. 
    But in production would be using a dynamic loop instead, rather than a hard coded wait time. 
    """

    # Get all the spans the registration element
    b.find_element(By.XPATH, "//span[contains(text(), 'Sign up')]").click()
    time.sleep(3)

    # Verify we're at the registration page
    if not b.find_element(By.XPATH,
            "//p[contains(text(),'Save looks, add products to your Favorites, and get updates on sales and price drops.')]")\
            .is_displayed():
        assert False, "Unable to get to registration page after clicking Sign up"

    # Generate a random email
    email = random_email()

    # Insert into text field
    b.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(email)
    time.sleep(3)

    # Click continue
    b.find_element(By.XPATH, "//span[contains(text(), 'continue')]").click()
    time.sleep(3)

    # Enter a password
    password = generate_word(min_length=8)
    b.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(password)

    # Click sing up
    b.find_element(By.XPATH, "//span[contains(text(), 'sign up to begin shopping')]").click()
    time.sleep(3)

    # Verify landed on home page
    verify_landing(b)

    # Print out message passed and what browser
    print(f"[PASS][{browser}]  UI_automation")

    # Close browser
    b.close()

    # Return created user in case needed
    return email, password


""" --------------------------------------------------------------------------
Tests
----------------------------------------------------------------------------"""


def test_categories_names(b):
    """
    Verify the names of all the categories exists
    """

    # Loop through every item
    for category in categories_test_data_map:
        categories_element = b.find_element(By.CSS_SELECTOR, f"a[data-test-id='{category[0]}']")
        assert categories_element.text == category[1], f"Expected {category[1]} but got {categories_element.text}"

    # Verify expected categories
    print("[PASS] All Categories exists")


def test_verify_CSS(b):
    """
    Verify categories div comparing to a list of CSS checkpoints
    """
    for category in categories_test_data_map:
        categories_element = b.find_element(By.CSS_SELECTOR, f"a[data-test-id='{category[0]}']")

        css_to_check = [
            ["align-items", "center"],
            ["flex-direction", "row"],
            ["display", "inline-flex"],
            ["cursor", "pointer"],
            ["color", "rgba(0, 0, 0, 1)"],
            ["background-color", "rgba(0, 0, 0, 0)"],
        ]

        for css in css_to_check:
            assert categories_element.value_of_css_property(css[0]) == css[1], f"CSS {css[0]} expected to be {css[1]} but got {categories_element.value_of_css_property(css[0])}"

    print("[PASS] CSS check points")


def test_compare_images(b):
    """
    Get the screenshot of the categories div and compare to an expected screenshot
    """

    # Where to write the gotten screenshot
    gotten_sc = "tmp/screenshot_gotten.png"

    # Delete previous temp screenshot if exists
    if os.path.isfile(gotten_sc):
        os.remove(gotten_sc)

    # Get the div screenshot
    container_element = b.find_element(By.CSS_SELECTOR, ".v-main .container.pt-0.pt-md-6")
    with open("tmp/screenshot_gotten.png", "wb") as file:
        file.write(container_element.screenshot_as_png)

    # Load the images to compare
    expected = Image.open("data/screenshot_categories.png")
    gotten_image = Image.open(gotten_sc)

    # Resize in case if they are different
    width = 500
    height = 500
    expected = expected.resize((width, height))
    gotten_image = gotten_image.resize((width, height))

    # Convert to gray scale
    expected = expected.convert('L')
    gotten_image = gotten_image.convert('L')

    # Calculate the difference
    pixels1 = np.array(expected.getdata(), dtype=np.float64)
    pixels2 = np.array(gotten_image.getdata(), dtype=np.float64)
    diff = np.sum(np.abs(pixels1 - pixels2))
    percentage_diff = (diff / (255 * width * height)) * 100

    # Assert to standard
    acceptable_limit = 0.5   # In percent
    assert percentage_diff < acceptable_limit, f"Screenshot difference is beyond limit of {str(acceptable_limit)}%. Image too different."

    # Print
    print(f"[PASS] Screenshot compared passed, with {percentage_diff}% difference")


def Test_Shop_Navigation_menu(browser_name, email, password):
    # Get browser
    b = browser_setup(browser_name)

    # Login
    login(b, email, password)

    # Open Discover menu
    b.find_element(By.XPATH, "//span[contains(text(), 'Shop')]").click()
    time.sleep(3)

    # TESTS ------------------------------------------------------------------------------------

    # Verify categories text
    test_categories_names(b)

    # Verify CSS
    test_verify_CSS(b)

    # Verify via image comparison
    test_compare_images(b)


""" --------------------------------------------------------------------------
Entry point
----------------------------------------------------------------------------"""
if __name__ == '__main__':
    # The list of browsers to test
    """
    Commented out other browsers. Just going to use one for demo but code is capable of testing more browsers.
    """
    browsers_to_test = [
        "Chrome",
        # "Firefox",
        # "Safari"
    ]

    # Loop test through each browser
    for browser in browsers_to_test:
        """
        Tests are modular so that they can be run independently of each other
        """

        # UI Automation test
        email, password = UI_automation(browser)

        # Shop Navigation menu
        # email = ""     # Comment this out if want to use previously created adhoc value
        # password = ""  # Comment this out if want to use previously created adhoc value
        Test_Shop_Navigation_menu(browser, email, password)
