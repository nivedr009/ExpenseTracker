import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Add this import

class TestUserLoginErrorMessagewithIncorrectCredentials:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Use webdriver-manager to automatically download and set up ChromeDriver
        service = Service(ChromeDriverManager().install())  # Use ChromeDriverManager to handle ChromeDriver installation
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()

    def test_userLoginErrorMessagewithIncorrectCredentials(self):
        print("🔎 Opening login page...")
        self.driver.get("http://localhost:8000/login/")

        print("🧪 Entering username...")
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("nived")

        print("🧪 Entering incorrect password...")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("123456")  # Incorrect password

        print("🚀 Clicking login button...")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-dark")
        login_button.click()

        print("⏳ Waiting for error message...")
        try:
            error_element = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            error_text = error_element.text.strip()
            assert "invalid" in error_text.lower(), \
                f"❌ Error message doesn't contain 'invalid'. Found: {error_text}"
            print("✅ Error message displayed correctly:", error_text)
        except Exception as e:
            print("❌ Error message not found or didn't match expected content.")
            raise e
