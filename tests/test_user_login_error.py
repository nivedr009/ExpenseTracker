# Test login failure with incorrect credentials and error message check
import pytest
import time
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserLoginErrorMessagewithIncorrectCredentials:
    def setup_method(self, method):
        service = EdgeService(executable_path="C:\\Users\\NIVED\\Downloads\\edgedriver_win64\\msedgedriver.exe")
        self.driver = Edge(service=service)
        self.driver.maximize_window()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_userLoginErrorMessagewithIncorrectCredentials(self):
        self.driver.get("http://localhost:8000/login/")
        time.sleep(0.5)

        self.driver.find_element(By.NAME, "username").send_keys("nived")
        time.sleep(0.5)

        self.driver.find_element(By.NAME, "password").send_keys("123456")
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".btn-dark").click()
        time.sleep(2)

        # Wait for the error message to appear
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))  # Update class if different
            )
            assert "invalid" in error_element.text.lower(), \
                "❌ Error message does not contain 'invalid'. Found: " + error_element.text
            print("✅ Error message displayed correctly:", error_element.text)
        except Exception as e:
            print("❌ Error message not found or did not match expectation.")
            raise e
