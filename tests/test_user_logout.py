import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Add this import
import os  # For handling environment variables

class TestLogout:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Use webdriver-manager to automatically download and set up ChromeDriver
        service = Service(ChromeDriverManager().install())  # Use ChromeDriverManager to handle ChromeDriver installation
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)

    def teardown_method(self, method):
        self.driver.quit()

    def test_logout(self):
      print("🔍 Opening login page...")
      self.driver.get("http://web:8000/login/")

      print("🧑 Entering username...")
      username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
      username_input.send_keys(os.getenv("TEST_USERNAME", "nived"))

      print("🔑 Entering password...")
      password_input = self.driver.find_element(By.NAME, "password")
      password_input.send_keys(os.getenv("TEST_PASSWORD", "qwerty"))

      print("🚀 Clicking login button...")
      login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-dark")
      login_button.click()

      print("🧭 Clicking logout button to open modal...")
      logout_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
      logout_button.click()

      print("⏳ Waiting for modal logout confirmation link...")
      modal_logout_link = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "#logoutModal .modal-footer .btn-danger"))
      )
      
      print("🧹 Clicking logout in modal...")
      modal_logout_link.click()

      print("✅ Checking if redirected to login page...")
      self.wait.until(EC.presence_of_element_located((By.NAME, "username")))  # Ensure we're back on login
