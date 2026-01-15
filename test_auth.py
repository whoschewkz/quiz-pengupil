import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

BASE_URL = "http://localhost/quiz-pengupil"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()

# ================= LOGIN =================
@pytest.mark.parametrize("username,password,expect_redirect", [
    ("irul", "password_salah", False),   # LOG-03
    ("irul", "password_benar", True),    # LOG-01 (isi sesuai hash)
    ("nouser", "test", False),            # LOG-02
    ("", "", False),                      # LOG-04
])
def test_login(driver, username, password, expect_redirect):
    driver.get(f"{BASE_URL}/login.php")

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "InputPassword").clear()

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "InputPassword").send_keys(password)
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)

    if expect_redirect:
        assert "index.php" in driver.current_url
    else:
        assert "login.php" in driver.current_url or \
               "alert-danger" in driver.page_source

# ================= REGISTER =================
@pytest.mark.parametrize("name,email,username,password,repass,expected", [
    ("", "", "", "", "", "Data tidak boleh kosong"),      # REG-01
    ("Test", "test@mail.com", "irul", "123", "1234", "Password tidak sama"), # REG-02
    ("Test", "test@mail.com", "irul", "password123", "password123", "Username sudah terdaftar"), # REG-03
])
def test_register(driver, name, email, username, password, repass, expected):
    driver.get(f"{BASE_URL}/register.php")

    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "InputEmail").send_keys(email)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "InputPassword").send_keys(password)
    driver.find_element(By.ID, "InputRePassword").send_keys(repass)
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)
    assert expected.lower() in driver.page_source.lower()
