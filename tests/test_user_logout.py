import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Add this import
import os  # For handling environment variables

class TestUserLogout:
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

    def test_userLogout(self):
        print("🔎 Opening login page...")
        # Ensure that you update the URL to use the Docker container's service name or IP
        self.driver.get("http://web:8000/login/")  # Assuming 'web' is the Docker service name

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys(os.getenv("TEST_USERNAME", "nived"))

        print("🧪 Entering password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(os.getenv("TEST_PASSWORD", "qwerty"))

        print("🚀 Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-dark")
        login_button.click()

        # Wait until the element is visible and clickable
        sidebar_toggle = self.wait.until(EC.element_to_be_clickable((By.ID, "open-sidebar")))
        # Optionally scroll into view if needed
        self.driver.execute_script("arguments[0].scrollIntoView(true);", sidebar_toggle)
        sidebar_toggle.click()

        print("⏳ Waiting for 'Logout' link to appear...")
        logout_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
        print("✅ 'Logout' link is visible. Clicking it...")
        logout_link.click()

        print("⏳ Waiting for logout confirmation modal...")
        confirm_logout_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".container > .container > #logoutModal .btn-danger")))
        print("✅ Logout confirmation modal is visible. Clicking 'Confirm Logout' button...")
        confirm_logout_button.click()

        print("⏳ Waiting for redirection to login page...")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Login')]"))
            )
            print("✅ Successfully logged out. Redirected to login page.")
        except Exception as e:
            print("❌ Logout might have failed. Login page not found.")
            raise e

        # Assert URL contains 'login'
        current_url = self.driver.current_url.lower()
        print(f"🌐 Redirected to: {current_url}")
        assert "login" in current_url, \
            f"❌ Logout did not redirect to login page. URL: {current_url}"