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
    driver.get("http://127.0.0.1:8000/login.php")
    yield driver
    driver.quit()

# =========================
# L01 - LOGIN VALID
# =========================
def test_login_valid(driver):
    driver.find_element(By.NAME, "username").send_keys("user1")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)

    # Login berhasil → redirect terjadi
    assert "login.php" not in driver.current_url

# =========================
# L02 - LOGIN PASSWORD SALAH
# =========================
def test_login_wrong_password(driver):
    driver.find_element(By.NAME, "username").send_keys("user1")
    driver.find_element(By.NAME, "password").send_keys("salah")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)

    assert "gagal" in driver.page_source.lower()

# =========================
# L03 - LOGIN USER TIDAK TERDAFTAR
# =========================
def test_login_unregistered_email(driver):
    driver.find_element(By.NAME, "username").send_keys("tidakada")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)

    assert "gagal" in driver.page_source.lower()

# =========================
# L05 - LOGIN FIELD KOSONG
# =========================
def test_login_empty_field(driver):
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)

    assert "data tidak boleh kosong" in driver.page_source.lower()

# =========================
# L04 - LOGIN TANPA NAME (EDGE CASE)
# =========================
def test_login_without_name(driver):
    # Sesuai catatan kuis: name tidak wajib
    driver.find_element(By.NAME, "username").send_keys("user1")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)

    assert "login.php" not in driver.current_url
