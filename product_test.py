import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        # 🔴 PENTING: ukuran window besar
        options.add_argument("--window-size=1920,1080")
        # HAPUS baris ini jika ingin lihat browser
        options.add_argument("--headless")

        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 15)
        os.makedirs("screenshots", exist_ok=True)

    def test_view_products_and_detail(self):
        d = self.driver
        w = self.wait

        # 1. Navigate to URL
        d.get("http://automationexercise.com")

        # 2. Verify home page
        self.assertIn("Automation Exercise", d.title)

        # 3. Click Products
        w.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@href='/products']"))
        ).click()

        # 4. Verify ALL PRODUCTS page
        w.until(EC.visibility_of_element_located(
            (By.XPATH, "//h2[text()='All Products']"))
        )

        # 5. Products list visible
        products_section = w.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "features_items"))
        )
        self.assertTrue(products_section.is_displayed())

        # 📸 Screenshot 1 – All Products
        d.save_screenshot("screenshots/TC03_all_products.png")

        # 🔥 6. SCROLL ke produk pertama
        first_product = w.until(EC.presence_of_element_located(
            (By.XPATH, "(//div[@class='product-image-wrapper'])[1]"))
        )

        d.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_product)

        # 🔥 7. Klik View Product pakai JavaScript
        view_product = first_product.find_element(By.XPATH, ".//a[contains(text(),'View Product')]")
        d.execute_script("arguments[0].click();", view_product)

        # 8. Verify product detail page
        product_name = w.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='product-information']/h2"))
        )

        category = d.find_element(By.XPATH, "//p[contains(text(),'Category')]")
        price = d.find_element(By.XPATH, "//span/span")
        availability = d.find_element(By.XPATH, "//b[text()='Availability:']")
        condition = d.find_element(By.XPATH, "//b[text()='Condition:']")
        brand = d.find_element(By.XPATH, "//b[text()='Brand:']")

        self.assertTrue(product_name.is_displayed())
        self.assertTrue(category.is_displayed())
        self.assertTrue(price.is_displayed())
        self.assertTrue(availability.is_displayed())
        self.assertTrue(condition.is_displayed())
        self.assertTrue(brand.is_displayed())

        # 📸 Screenshot 2 – PRODUCT DETAIL (INI WAJIB UNTUK LAPORAN)
        d.save_screenshot("screenshots/TC03_product_detail.png")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
