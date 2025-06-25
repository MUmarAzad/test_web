from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
BASE_URL = "http://13.60.24.6:8081"

def test_homepage_loads():
    """Test Case 1: Verify homepage loads successfully."""
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("✅ Test Case 1: Homepage Load - Passed")
    except TimeoutException:
        print("❌ Test Case 1: Homepage Load - Failed (Timeout)")
    except Exception as e:
        print(f"❌ Test Case 1: Homepage Load - Failed due to {str(e)}")

def test_product_listing_accessibility():
    """Test Case 2: Check product listing page accessibility."""
    try:
        driver.get(f"{BASE_URL}/shop")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        print("✅ Test Case 2: Product Listing Accessibility - Passed")
    except TimeoutException:
        print("❌ Test Case 2: Product Listing Accessibility - Failed (Timeout)")
    except NoSuchElementException:
        print("❌ Test Case 2: Product Listing Accessibility - Failed (Element not found)")
    except Exception as e:
        print(f"❌ Test Case 2: Product Listing Accessibility - Failed due to {str(e)}")

def test_login_success():
    """Test Case 3: Validate user login with correct credentials."""
    try:
        driver.get(BASE_URL)
        login_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Login')]"))
        )
        login_link.click()
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        email_field.send_keys("umar.azad.work@gmail.com")
        password_field.send_keys("Umar2004Azad")
        login_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        print("✅ Test Case 3: Login Success - Passed")
    except TimeoutException:
        print("❌ Test Case 3: Login Success - Failed (Timeout)")
    except NoSuchElementException:
        print("❌ Test Case 3: Login Success - Failed (Element not found)")
    except Exception as e:
        print(f"❌ Test Case 3: Login Success - Failed due to {str(e)}")

def test_login_failure():
    """Test Case 4: Test login failure with invalid credentials."""
    try:
        driver.get(BASE_URL)
        login_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Login')]"))
        )
        login_link.click()
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        email_field.send_keys("umar.azad.work@gmail.com")
        password_field.send_keys("wrongpass")
        login_button.click()
        error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "error")))
        assert "invalid" in error_message.text.lower()
        print("✅ Test Case 4: Login Failure - Passed")
    except TimeoutException:
        print("❌ Test Case 4: Login Failure - Failed (Timeout)")
    except AssertionError:
        print("❌ Test Case 4: Login Failure - Failed (Assertion)")
    except Exception as e:
        print(f"❌ Test Case 4: Login Failure - Failed due to {str(e)}")

def test_product_search():
    """Test Case 5: Ensure product search functionality works."""
    try:
        driver.get(f"{BASE_URL}/shop")
        search_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
        search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
        search_field.send_keys("modern")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'modern')]")))
        print("✅ Test Case 5: Product Search - Passed")
    except TimeoutException:
        print("❌ Test Case 5: Product Search - Failed (Timeout)")
    except NoSuchElementException:
        print("❌ Test Case 5: Product Search - Failed (Element not found)")
    except Exception as e:
        print(f"❌ Test Case 5: Product Search - Failed due to {str(e)}")

def test_add_to_cart():
    """Test Case 6: Verify adding a product to the cart."""
    try:
        driver.get(f"{BASE_URL}/shop")
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Add to Cart')]"))
        )
        add_to_cart_button.click()
        # Assuming cart panel opens; look for cart indicator
        cart_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart-count")))
        assert int(cart_count.text) > 0
        print("✅ Test Case 6: Add to Cart - Passed")
    except TimeoutException:
        print("❌ Test Case 6: Add to Cart - Failed (Timeout)")
    except AssertionError:
        print("❌ Test Case 6: Add to Cart - Failed (Assertion)")
    except Exception as e:
        print(f"❌ Test Case 6: Add to Cart - Failed due to {str(e)}")

def test_cart_removal():
    """Test Case 7: Test cart removal functionality."""
    try:
        driver.get(f"{BASE_URL}/shop")
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Add to Cart')]"))
        )
        add_to_cart_button.click()
        remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Remove')]")))
        remove_button.click()
        cart_count = driver.find_element(By.CLASS_NAME, "cart-count")
        assert int(cart_count.text) == 0 or cart_count.text == ""
        print("✅ Test Case 7: Cart Removal - Passed")
    except TimeoutException:
        print("❌ Test Case 7: Cart Removal - Failed (Timeout)")
    except AssertionError:
        print("❌ Test Case 7: Cart Removal - Failed (Assertion)")
    except Exception as e:
        print(f"❌ Test Case 7: Cart Removal - Failed due to {str(e)}")

def test_checkout_initiation():
    """Test Case 8: Check checkout process initiation (Place Order)."""
    try:
        driver.get(f"{BASE_URL}/shop")
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Add to Cart')]"))
        )
        add_to_cart_button.click()
        place_order_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Place Order')]")))
        place_order_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "form")))  # Assuming a form for order details
        print("✅ Test Case 8: Checkout Initiation - Passed")
    except TimeoutException:
        print("❌ Test Case 8: Checkout Initiation - Failed (Timeout)")
    except NoSuchElementException:
        print("❌ Test Case 8: Checkout Initiation - Failed (Element not found)")
    except Exception as e:
        print(f"❌ Test Case 8: Checkout Initiation - Failed due to {str(e)}")

def test_user_registration():
    """Test Case 9: Validate user registration form submission (avoiding deletion)."""
    try:
        driver.get(BASE_URL)
        register_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Register')]"))
        )
        register_link.click()
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        register_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
        email_field.send_keys("testuser@gmail.com")  # Unique test email
        password_field.send_keys("newpass123")
        register_button.click()
        # Check for success without assuming deletion
        success_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "success")))
        assert "successful" in success_message.text.lower()
        print("✅ Test Case 9: User Registration - Passed")
    except TimeoutException:
        print("❌ Test Case 9: User Registration - Failed (Timeout)")
    except AssertionError:
        print("❌ Test Case 9: User Registration - Failed (Assertion)")
    except Exception as e:
        print(f"❌ Test Case 9: User Registration - Failed due to {str(e)}")

def test_footer_links():
    """Test Case 10: Ensure footer links are clickable."""
    try:
        driver.get(BASE_URL)
        footer_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//footer//a")))
        footer_link.click()
        print("✅ Test Case 10: Footer Links - Passed")
    except TimeoutException:
        print("❌ Test Case 10: Footer Links - Failed (Timeout)")
    except NoSuchElementException:
        print("❌ Test Case 10: Footer Links - Failed (Element not found)")
    except Exception as e:
        print(f"❌ Test Case 10: Footer Links - Failed due to {str(e)}")

if __name__ == "__main__":
    test_cases = [
        test_homepage_loads,
        test_product_listing_accessibility,
        test_login_success,
        test_login_failure,
        test_product_search,
        test_add_to_cart,
        test_cart_removal,
        test_checkout_initiation,
        test_user_registration,
        test_footer_links
    ]
    
    for test in test_cases:
        test()
    
    driver.quit()