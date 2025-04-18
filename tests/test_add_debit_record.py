import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Add this import
import os  # For handling environment variables

class TestAddDebitRecord:
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

    def test_addDebitRecord(self):
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

        print("⏳ Waiting for '+ Add Record' link to appear...")
        add_record_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "+ Add Record")))
        print("✅ '+ Add Record' link is visible. Clicking it...")
        add_record_link.click()

        print("🧾 Switching to 'Debit' tab...")
        debit_tab = self.wait.until(EC.presence_of_element_located((By.ID, "debit-tab")))
        debit_tab.click()

        print("🧾 Selecting category...")
        category_dropdown = self.wait.until(EC.presence_of_element_located((By.ID, "id_category")))
        category_dropdown.click()
        category_dropdown.find_element(By.XPATH, "//option[. = 'Entertainment']").click()

        print("💰 Entering amount...")
        amount_input = self.driver.find_element(By.ID, "id_amount")
        amount_input.send_keys("250")

        print("📝 Entering description...")
        description_input = self.driver.find_element(By.ID, "id_description")
        description_input.send_keys("Movie")

        print("🚀 Clicking 'Add Transaction' button...")
        add_transaction_button = self.driver.find_element(By.ID, "add-transaction-btn")
        add_transaction_button.click()

        print("⏳ Waiting for confirmation modal to close...")
        close_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-close:nth-child(1)")))
        close_button.click()

        print("⏳ Waiting for 'Back to Dashboard' link to appear...")
        back_to_dashboard_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Back to Dashboard")))
        print("✅ 'Back to Dashboard' link is visible. Clicking it...")
        back_to_dashboard_link.click()

        print("⏳ Waiting for redirection to dashboard...")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]"))
            )
            print("✅ Successfully added debit record. Redirected to dashboard.")
        except Exception as e:
            print("❌ Failed to add debit record. Dashboard not found.")
            raise e

        # Assert URL contains 'dashboard'
        current_url = self.driver.current_url.lower()
        print(f"🌐 Redirected to: {current_url}")
        assert "dashboard" in current_url, \
            f"❌ Adding debit record did not redirect to dashboard. URL: {current_url}"