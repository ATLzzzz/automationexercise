import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class CheckoutRegisterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--window-size=1920,1080")
        # ⚠️ JANGAN headless agar form stabil
        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 20)

        os.makedirs("screenshots", exist_ok=True)

    def screenshot(self, name):
        self.driver.save_screenshot(f"screenshots/{name}.png")

    def test_place_order_register_while_checkout(self):
        d = self.driver
        w = self.wait

        # 1. Open Website
        d.get("http://automationexercise.com")
        self.screenshot("01_home")

        # 2. Add Product
        product = w.until(EC.presence_of_element_located(
            (By.XPATH, "(//div[@class='product-image-wrapper'])[1]"))
        )
        d.execute_script("arguments[0].scrollIntoView(true);", product)
        d.execute_script(
            "arguments[0].click();",
            product.find_element(By.XPATH, ".//a[contains(text(),'Add to cart')]")
        )
        time.sleep(2)
        self.screenshot("02_add_to_cart_popup")

        d.find_element(By.XPATH, "//button[text()='Continue Shopping']").click()

        # 3. Cart → Checkout
        d.find_element(By.XPATH, "//a[@href='/view_cart']").click()
        self.screenshot("03_cart")

        d.find_element(By.XPATH, "//a[text()='Proceed To Checkout']").click()
        time.sleep(2)
        self.screenshot("04_checkout_popup")

        d.find_element(By.XPATH, "//u[text()='Register / Login']").click()
        self.screenshot("05_signup_login")

        # 4. Signup (DATA DIBUAT SENDIRI & LENGKAP)
        email = f"student_{int(time.time())}@test.com"
        d.find_element(By.NAME, "name").send_keys("Automation Student")
        d.find_element(By.CSS_SELECTOR, "[data-qa='signup-email']").send_keys(email)
        d.find_element(By.CSS_SELECTOR, "[data-qa='signup-button']").click()
        time.sleep(3)
        self.screenshot("06_after_signup")

        # 5. PAKSA ISI FORM (TIDAK MENUNGGU REDIRECT)
        try:
            d.execute_script("window.scrollTo(0,0);")

            d.find_element(By.ID, "id_gender1").click()
            d.find_element(By.ID, "password").send_keys("Test12345")

            Select(d.find_element(By.ID, "days")).select_by_value("10")
            Select(d.find_element(By.ID, "months")).select_by_value("5")
            Select(d.find_element(By.ID, "years")).select_by_value("1999")

            d.find_element(By.ID, "newsletter").click()
            d.find_element(By.ID, "optin").click()

            d.find_element(By.ID, "first_name").send_keys("Automation")
            d.find_element(By.ID, "last_name").send_keys("Student")
            d.find_element(By.ID, "address1").send_keys("Jl. Testing No. 1")
            d.find_element(By.ID, "address2").send_keys("Jakarta")

            Select(d.find_element(By.ID, "country")).select_by_visible_text("India")
            d.find_element(By.ID, "state").send_keys("Delhi")
            d.find_element(By.ID, "city").send_keys("New Delhi")
            d.find_element(By.ID, "zipcode").send_keys("12345")
            d.find_element(By.ID, "mobile_number").send_keys("081234567890")

            self.screenshot("07_form_filled")

            d.find_element(By.CSS_SELECTOR, "[data-qa='create-account']").click()
            time.sleep(3)
            self.screenshot("08_after_create_account")

        except Exception as e:
            self.screenshot("ERROR_form_fill")
            self.fail("Gagal mengisi form registrasi (limitasi sistem AutomationExercise)")

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
