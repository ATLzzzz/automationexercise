import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

class RegisterTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        #options.add_argument("--headless")  # hapus jika ingin lihat browser
        cls.browser = webdriver.Chrome(options=options)
        cls.browser.implicitly_wait(10)

        # Buat folder screenshot jika belum ada
        os.makedirs("screenshots", exist_ok=True)

    def test_register_user_end_to_end(self):
        driver = self.browser

        driver.get("http://automationexercise.com")
        self.assertIn("Automation Exercise", driver.title)

        driver.find_element(By.LINK_TEXT, "Signup / Login").click()

        signup_text = driver.find_element(By.CLASS_NAME, "signup-form") \
                            .find_element(By.TAG_NAME, "h2").text
        self.assertIn("New User Signup!", signup_text)

        driver.find_element(By.NAME, "name").send_keys("actest")
        driver.find_element(By.CSS_SELECTOR, "[data-qa='signup-email']").send_keys("actest@email.com")
        driver.find_element(By.CSS_SELECTOR, "[data-qa='signup-button']").click()

        account_info = driver.find_element(By.XPATH, "//div[@class='login-form']/h2/b").text
        self.assertIn("ENTER ACCOUNT INFORMATION", account_info)

        driver.find_element(By.ID, "id_gender1").click()
        driver.find_element(By.ID, "password").send_keys("Aria123")

        driver.find_element(By.ID, "newsletter").click()
        driver.find_element(By.ID, "optin").click()

        driver.find_element(By.ID, "first_name").send_keys("Account")
        driver.find_element(By.ID, "last_name").send_keys("Test")
        driver.find_element(By.ID, "address1").send_keys("Windavan")
        driver.find_element(By.XPATH, "//select[@name='country']/option[@value='India']").click()
        driver.find_element(By.ID, "state").send_keys("Vraj")
        driver.find_element(By.ID, "city").send_keys("Radha")
        driver.find_element(By.ID, "zipcode").send_keys("11100")
        driver.find_element(By.ID, "mobile_number").send_keys("0765432314")

        driver.find_element(By.CSS_SELECTOR, "[data-qa='create-account']").click()

        created_text = driver.find_element(By.CSS_SELECTOR, "[data-qa='account-created']").text
        self.assertIn("ACCOUNT CREATED!", created_text)

    def tearDown(self):
        # Screenshot setiap selesai test
        test_name = self._testMethodName
        self.browser.save_screenshot(f"screenshots/{test_name}.png")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == "__main__":
    unittest.main()
