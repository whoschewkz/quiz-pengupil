import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:80/register.php")
    yield driver
    driver.quit()

# =========================
# POSITIVE TEST
# =========================
def test_register_valid(driver):
    driver.find_element(By.NAME, "name").send_keys("User Satu")
    driver.find_element(By.NAME, "email").send_keys("user1@example.com")
    driver.find_element(By.NAME, "username").send_keys("user1")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "repassword").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "berhasil" in driver.page_source.lower()

# =========================
# NEGATIVE TESTS
# =========================
def test_register_duplicate_email(driver):
    driver.find_element(By.NAME, "name").send_keys("User Duplicate")
    driver.find_element(By.NAME, "email").send_keys("user1@example.com")
    driver.find_element(By.NAME, "username").send_keys("userdup")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "repassword").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "sudah" in driver.page_source.lower()

def test_register_email_empty(driver):
    driver.find_element(By.NAME, "name").send_keys("No Email")
    driver.find_element(By.NAME, "username").send_keys("noemail")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "repassword").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "email" in driver.page_source.lower()

def test_register_password_empty(driver):
    driver.find_element(By.NAME, "name").send_keys("No Password")
    driver.find_element(By.NAME, "email").send_keys("nopass@example.com")
    driver.find_element(By.NAME, "username").send_keys("nopass")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "password" in driver.page_source.lower()

def test_register_without_name(driver):
    driver.find_element(By.NAME, "email").send_keys("noname@example.com")
    driver.find_element(By.NAME, "username").send_keys("noname")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "repassword").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "nama" in driver.page_source.lower()
