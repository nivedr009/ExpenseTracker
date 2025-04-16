# Updated test with delays and better assertion
import pytest
import time
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserLoginwithCorrectCredentials:
    def setup_method(self, method):
        service = EdgeService(executable_path="C:\\Users\\NIVED\\Downloads\\edgedriver_win64\\msedgedriver.exe")
        self.driver = Edge(service=service)
        self.driver.maximize_window()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_userLoginwithCorrectCredentials(self):
        self.driver.get("http://localhost:8000/login/")
        time.sleep(0.5)

        self.driver.find_element(By.NAME, "username").send_keys("nived")
        time.sleep(0.5)

        self.driver.find_element(By.NAME, "password").send_keys("qwerty")
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".btn-dark").click()
        time.sleep(2)

        # Wait for a dashboard element to confirm successful login
        try:
            dashboard_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]"))
            )
            print("✅ Successfully logged in. Dashboard is visible.")
        except Exception as e:
            print("❌ Login might have failed. Dashboard element not found.")
            raise e

        # Assert that the URL indicates dashboard or home
        assert "dashboard" in self.driver.current_url.lower() or "home" in self.driver.current_url.lower(), \
            "❌ Login did not redirect to dashboard/home. Current URL: " + self.driver.current_url
