import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class LoginPositiveTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        #options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)
        os.makedirs("screenshots", exist_ok=True)

    def test_login_valid_user(self):
        d = self.driver
        d.get("http://automationexercise.com")

        d.find_element(By.LINK_TEXT, "Signup / Login").click()
        d.find_element(By.CSS_SELECTOR, "[data-qa='login-email']").send_keys("actest@email.com")
        d.find_element(By.CSS_SELECTOR, "[data-qa='login-password']").send_keys("Aria123")
        d.find_element(By.CSS_SELECTOR, "[data-qa='login-button']").click()

        logged = d.find_element(By.XPATH, "//a[contains(text(),'Logged in as')]").text
        self.assertIn("actest", logged)

    def tearDown(self):
        self.driver.save_screenshot("screenshots/login_positive.png")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
