import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestLogout():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
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

    # Wait for the logout modal to be visible and interactable
    modal = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "logoutModal"))
    )
    
    # Scroll to the logout button in case it is out of view
    logout_button = modal.find_element(By.CSS_SELECTOR, ".btn-danger")
    self.driver.execute_script("arguments[0].scrollIntoView(true);", logout_button)

    # Wait for the logout button to be clickable and then click it
    logout_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-danger"))
    )
    logout_button.click()
