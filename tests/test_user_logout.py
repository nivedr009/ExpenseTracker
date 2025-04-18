from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytest
import time

class TestLogout:

    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--remote-debugging-port=9222')

        # This assumes chromedriver is installed at /usr/local/bin/chromedriver
        service = Service("/usr/local/bin/chromedriver")

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("http://web:8000/login")  # use container name in Docker network

    def teardown_method(self, method):
        self.driver.quit()

    def test_logout(self):
        driver = self.driver

        # Simulate login
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("testpass")
        driver.find_element(By.ID, "login-button").click()

        time.sleep(2)

        # Click logout
        driver.find_element(By.ID, "logout-button").click()

        time.sleep(2)

        # Check if redirected to login page
        assert "Login" in driver.title or "login" in driver.current_url
