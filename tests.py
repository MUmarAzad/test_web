import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

BASE_URL = os.getenv("BASE_URL", "http://13.60.24.6:8081")

class EcommerceE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.wait = WebDriverWait(cls.driver, 20)  # Increased timeout

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage_loads(self):
        """Test 1: Homepage loads successfully."""
        try:
            self.driver.get(BASE_URL)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("✅ Test 1: Homepage Load - Passed")
        except (TimeoutException, Exception) as e:
            print(f"❌ Test 1: Homepage Load - Failed due to {str(e)}")
            self.fail()

    def test_product_listing_accessibility(self):
        """Test 2: Product listing page is accessible."""
        try:
            self.driver.get(f"{BASE_URL}/shop")
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-list")))
            print("✅ Test 2: Product Listing Accessibility - Passed")
        except (TimeoutException, NoSuchElementException, Exception) as e:
            print(f"❌ Test 2: Product Listing Accessibility - Failed due to {str(e)}")
            self.fail()

    def test_user_registration(self):
        """Test 3: User registration form submission with unique email."""
        try:
            self.driver.get(BASE_URL)
            register_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Register')]")))
            register_link.click()
            unique_email = f"testuser_{int(time.time())}@example.com"  # Unique email with timestamp
            email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form-group input[type='email']")))
            password_field = self.driver.find_element(By.CSS_SELECTOR, ".form-group input[type='password']")
            register_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
            email_field.send_keys(unique_email)
            password_field.send_keys(os.getenv("TEST_PASSWORD", "newpass123"))
            register_button.click()
            success_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "success")))
            self.assertIn("successful", success_message.text.lower())
            print(f"✅ Test 3: User Registration - Passed with email {unique_email}")
            # Store credentials for next test
            self.registered_email = unique_email
            self.registered_password = os.getenv("TEST_PASSWORD", "newpass123")
        except (TimeoutException, NoSuchElementException, AssertionError, Exception) as e:
            print(f"❌ Test 3: User Registration - Failed due to {str(e)}")
            self.fail()

    def test_login_success(self):
        """Test 4: User can log in with newly registered credentials."""
        try:
            if not hasattr(self, 'registered_email'):  # Skip if registration failed
                raise Exception("Registration failed, skipping login test")
            self.driver.get(BASE_URL)
            login_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]")))
            login_link.click()
            email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form-group input[type='email']")))
            password_field = self.driver.find_element(By.CSS_SELECTOR, ".form-group input[type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            email_field.send_keys(self.registered_email)
            password_field.send_keys(self.registered_password)
            login_button.click()
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
            print("✅ Test 4: Login Success - Passed")
        except (TimeoutException, NoSuchElementException, Exception) as e:
            print(f"❌ Test 4: Login Success - Failed due to {str(e)}")
            self.fail()

    def test_login_failure(self):
        """Test 5: Login fails with invalid credentials."""
        try:
            self.driver.get(BASE_URL)
            login_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]")))
            login_link.click()
            email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form-group input[type='email']")))
            password_field = self.driver.find_element(By.CSS_SELECTOR, ".form-group input[type='password']")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            email_field.send_keys("invalid@example.com")
            password_field.send_keys("wrongpass")
            login_button.click()
            error_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "error")))
            self.assertIn("invalid", error_message.text.lower())
            print("✅ Test 5: Login Failure - Passed")
        except (TimeoutException, NoSuchElementException, AssertionError, Exception) as e:
            print(f"❌ Test 5: Login Failure - Failed due to {str(e)}")
            self.fail()

    def test_product_search(self):
        """Test 6: Product search works."""
        try:
            self.driver.get(f"{BASE_URL}/shop")
            search_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
            search_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
            search_field.send_keys("modern")
            search_button.click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'modern')]")))
            print("✅ Test 6: Product Search - Passed")
        except (TimeoutException, NoSuchElementException, Exception) as e:
            print(f"❌ Test 6: Product Search - Failed due to {str(e)}")
            self.fail()

    def test_add_to_cart(self):
        """Test 7: Add product to cart."""
        try:
            self.driver.get(f"{BASE_URL}/shop")
            add_to_cart_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.add-to-cart")))
            add_to_cart_button.click()
            cart_count = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart-count")))
            self.assertGreater(int(cart_count.text), 0)
            print("✅ Test 7: Add to Cart - Passed")
        except (TimeoutException, NoSuchElementException, AssertionError, Exception) as e:
            print(f"❌ Test 7: Add to Cart - Failed due to {str(e)}")
            self.fail()

    def test_cart_removal(self):
        """Test 8: Remove product from cart."""
        try:
            self.driver.get(f"{BASE_URL}/shop")
            add_to_cart_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.add-to-cart")))
            add_to_cart_button.click()
            remove_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.remove")))
            remove_button.click()
            cart_count = self.driver.find_element(By.CLASS_NAME, "cart-count")
            self.assertTrue(cart_count.text == "" or int(cart_count.text) == 0)
            print("✅ Test 8: Cart Removal - Passed")
        except (TimeoutException, NoSuchElementException, AssertionError, Exception) as e:
            print(f"❌ Test 8: Cart Removal - Failed due to {str(e)}")
            self.fail()

    def test_checkout_initiation(self):
        """Test 9: Initiate checkout process."""
        try:
            self.driver.get(f"{BASE_URL}/shop")
            add_to_cart_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.add-to-cart")))
            add_to_cart_button.click()
            place_order_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.place-order")))
            place_order_button.click()
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
            print("✅ Test 9: Checkout Initiation - Passed")
        except (TimeoutException, NoSuchElementException, Exception) as e:
            print(f"❌ Test 9: Checkout Initiation - Failed due to {str(e)}")
            self.fail()

    def test_footer_links(self):
        """Test 10: Footer links are clickable."""
        try:
            self.driver.get(BASE_URL)
            footer_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//footer//a")))
            footer_link.click()
            print("✅ Test 10: Footer Links - Passed")
        except (TimeoutException, NoSuchElementException, Exception) as e:
            print(f"❌ Test 10: Footer Links - Failed due to {str(e)}")
            self.fail()

if __name__ == "__main__":
    unittest.main()