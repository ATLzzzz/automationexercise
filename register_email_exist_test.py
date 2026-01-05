import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

class RegisterNegativeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        #options.add_argument("--headless")
        cls.browser = webdriver.Chrome(options=options)
        cls.browser.implicitly_wait(10)

        os.makedirs("screenshots", exist_ok=True)

    def test_register_with_existing_email(self):
        driver = self.browser

        driver.get("http://automationexercise.com")
        driver.find_element(By.LINK_TEXT, "Signup / Login").click()

        driver.find_element(By.NAME, "name").send_keys("actest")
        driver.find_element(By.CSS_SELECTOR, "[data-qa='signup-email']").send_keys("actest@email.com")
        driver.find_element(By.CSS_SELECTOR, "[data-qa='signup-button']").click()

        error_text = driver.find_element(By.XPATH, "//p[text()='Email Address already exist!']").text
        self.assertIn("Email Address already exist!", error_text)

    def tearDown(self):
        test_name = self._testMethodName
        self.browser.save_screenshot(f"screenshots/{test_name}.png")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == "__main__":
    unittest.main()
