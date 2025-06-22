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
BASE_URL = "http://13.60.24.6:8080"

def test_homepage_loads():
    """Test Case 1: Verify homepage loads successfully."""
    try:
        driver.get(BASE_URL)
        assert "MERN Store" in driver.title
        print("Test Case 1: Homepage Load - Passed")
    except AssertionError:
        print("Test Case 1: Homepage Load - Failed")
    except Exception as e:
        print(f"Test Case 1: Homepage Load - Failed due to {str(e)}")

def test_product_listing_accessibility():
    """Test Case 2: Check product listing page accessibility."""
    try:
        driver.get(f"{BASE_URL}/products")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-list")))
        print("Test Case 2: Product Listing Accessibility - Passed")
    except TimeoutException:
        print("Test Case 2: Product Listing Accessibility - Failed (Timeout)")
    except NoSuchElementException:
        print("Test Case 2: Product Listing Accessibility - Failed (Element not found)")
    except Exception as e:
        print(f"Test Case 2: Product Listing Accessibility - Failed due to {str(e)}")

def test_login_success():
    """Test Case 3: Validate user login with correct credentials."""
    try:
        driver.get(f"{BASE_URL}/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys("testuser@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "login-btn").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "welcome-message")))
        print("Test Case 3: Login Success - Passed")
    except TimeoutException:
        print("Test Case 3: Login Success - Failed (Timeout)")
    except NoSuchElementException:
        print("Test Case 3: Login Success - Failed (Element not found)")
    except Exception as e:
        print(f"Test Case 3: Login Success - Failed due to {str(e)}")

def test_login_failure():
    """Test Case 4: Test login failure with invalid credentials."""
    try:
        driver.get(f"{BASE_URL}/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys("invalid@example.com")
        driver.find_element(By.ID, "password").send_keys("wrongpass")
        driver.find_element(By.ID, "login-btn").click()
        error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "error-message")))
        assert "Invalid credentials" in error_message.text
        print("Test Case 4: Login Failure - Passed")
    except TimeoutException:
        print("Test Case 4: Login Failure - Failed (Timeout)")
    except AssertionError:
        print("Test Case 4: Login Failure - Failed (Assertion)")
    except Exception as e:
        print(f"Test Case 4: Login Failure - Failed due to {str(e)}")

def test_product_search():
    """Test Case 5: Ensure product search functionality works."""
    try:
        driver.get(f"{BASE_URL}/products")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-bar"))).send_keys("shirt")
        driver.find_element(By.ID, "search-btn").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'shirt')]")))
        print("Test Case 5: Product Search - Passed")
    except TimeoutException:
        print("Test Case 5: Product Search - Failed (Timeout)")
    except NoSuchElementException:
        print("Test Case 5: Product Search - Failed (Element not found)")
    except Exception as e:
        print(f"Test Case 5: Product Search - Failed due to {str(e)}")

def test_add_to_cart():
    """Test Case 6: Verify adding a product to the cart."""
    try:
        driver.get(f"{BASE_URL}/products")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "add-to-cart-btn"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cart-count")))
        assert int(driver.find_element(By.ID, "cart-count").text) > 0
        print("Test Case 6: Add to Cart - Passed")
    except TimeoutException:
        print("Test Case 6: Add to Cart - Failed (Timeout)")
    except AssertionError:
        print("Test Case 6: Add to Cart - Failed (Assertion)")
    except Exception as e:
        print(f"Test Case 6: Add to Cart - Failed due to {str(e)}")

def test_cart_removal():
    """Test Case 7: Test cart removal functionality."""
    try:
        driver.get(f"{BASE_URL}/cart")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "remove-item-btn"))).click()
        cart_count = driver.find_element(By.ID, "cart-count")
        assert int(cart_count.text) == 0 or cart_count.text == ""
        print("Test Case 7: Cart Removal - Passed")
    except TimeoutException:
        print("Test Case 7: Cart Removal - Failed (Timeout)")
    except AssertionError:
        print("Test Case 7: Cart Removal - Failed (Assertion)")
    except Exception as e:
        print(f"Test Case 7: Cart Removal - Failed due to {str(e)}")

def test_checkout_initiation():
    """Test Case 8: Check checkout process initiation."""
    try:
        driver.get(f"{BASE_URL}/cart")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout-btn"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout-page")))
        print("Test Case 8: Checkout Initiation - Passed")
    except TimeoutException:
        print("Test Case 8: Checkout Initiation - Failed (Timeout)")
    except NoSuchElementException:
        print("Test Case 8: Checkout Initiation - Failed (Element not found)")
    except Exception as e:
        print(f"Test Case 8: Checkout Initiation - Failed due to {str(e)}")

def test_user_registration():
    """Test Case 9: Validate user registration form submission."""
    try:
        driver.get(f"{BASE_URL}/register")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys("newuser@example.com")
        driver.find_element(By.ID, "password").send_keys("newpass123")
        driver.find_element(By.ID, "register-btn").click()
        success_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "success-message")))
        assert "Registration successful" in success_message.text
        print("Test Case 9: User Registration - Passed")
    except TimeoutException:
        print("Test Case 9: User Registration - Failed (Timeout)")
    except AssertionError:
        print("Test Case 9: User Registration - Failed (Assertion)")
    except Exception as e:
        print(f"Test Case 9: User Registration - Failed due to {str(e)}")

def test_footer_links():
    """Test Case 10: Ensure footer links are clickable."""
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "footer-link"))).click()
        print("Test Case 10: Footer Links - Passed")
    except TimeoutException:
        print("Test Case 10: Footer Links - Failed (Timeout)")
    except NoSuchElementException:
        print("Test Case 10: Footer Links - Failed (Element not found)")
    except Exception as e:
        print(f"Test Case 10: Footer Links - Failed due to {str(e)}")

# Run all test cases
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