import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager  # To manage ChromeDriver

class TestLogout():
    def setup_method(self, method):
        # Set up Chrome options for headless operation
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")  # Needed for certain CI environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid issues in Docker

        # Use webdriver-manager to automatically download and set up ChromeDriver
        service = Service(ChromeDriverManager().install())  # Automatically manage ChromeDriver version
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.vars = {}
    
    def teardown_method(self, method):
        self.driver.quit()
    
    def test_logout(self):
        # Open the login page
        self.driver.get("http://web:8000/login/")
        self.driver.set_window_size(1057, 800)  # Set the window size

        # Enter username and password (hardcoded)
        self.driver.find_element(By.NAME, "username").click()
        self.driver.find_element(By.NAME, "username").send_keys("nived")
        self.driver.find_element(By.NAME, "password").click()
        self.driver.find_element(By.NAME, "password").send_keys("qwerty")

        # Click the login button
        self.driver.find_element(By.CSS_SELECTOR, ".btn-dark").click()

        # Click on the logout link
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

        # Confirm the logout in the modal
        self.driver.find_element(By.CSS_SELECTOR, ".container > .container > #logoutModal .btn-danger").click()
