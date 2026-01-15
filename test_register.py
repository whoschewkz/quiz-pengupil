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
    driver.get("http://localhost:8000/register.php")
    yield driver
    driver.quit()

# =========================
# R01 - REGISTER FIELD KOSONG
# =========================
def test_register_empty_all(driver):
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    assert "data tidak boleh kosong" in driver.page_source.lower()

# =========================
# R02 - PASSWORD TIDAK SAMA
# =========================
def test_register_password_mismatch(driver):
    driver.find_element(By.NAME, "name").send_keys("User Test")
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "username").send_keys("testuser")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "repassword").send_keys("654321")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "password tidak sama" in driver.page_source.lower()

# =========================
# R03 - EMAIL KOSONG
# =========================
def test_register_email_empty(driver):
    driver.find_element(By.NAME, "name").send_keys("No Email")
    driver.find_element(By.NAME, "username").send_keys("noemail")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "repassword").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "data tidak boleh kosong" in driver.page_source.lower()

# =========================
# R04 - PASSWORD KOSONG
# =========================
def test_register_password_empty(driver):
    driver.find_element(By.NAME, "name").send_keys("No Password")
    driver.find_element(By.NAME, "email").send_keys("nopass@example.com")
    driver.find_element(By.NAME, "username").send_keys("nopass")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "data tidak boleh kosong" in driver.page_source.lower()

# =========================
# R05 - TANPA NAMA
# =========================
def test_register_without_name(driver):
    driver.find_element(By.NAME, "email").send_keys("noname@example.com")
    driver.find_element(By.NAME, "username").send_keys("noname")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "repassword").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "data tidak boleh kosong" in driver.page_source.lower()
