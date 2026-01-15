import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

BASE_URL = "http://localhost"

# ======================
# SETUP DRIVER (STUB)
# ======================
@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()

# ======================
# REGISTER TEST CASES
# ======================
@pytest.mark.parametrize("username,email,password,expected", [
    ("user123", "user@mail.com", "password123", "success"),      # REG-01
    ("", "user@mail.com", "password123", "error"),               # REG-02
    ("user123", "invalid@", "password123", "error"),             # REG-03
    ("user123", "user@mail.com", "123", "error"),                # REG-04
    ("existinguser", "exist@mail.com", "password123", "error")  # REG-05
])
def test_register(driver, username, email, password, expected):
    driver.get(f"{BASE_URL}/register")

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "submit").click()

    time.sleep(1)

    assert expected in driver.page_source.lower()

# ======================
# LOGIN TEST CASES
# ======================
@pytest.mark.parametrize("username,password,expected", [
    ("user123", "password123", "dashboard"),       # LOG-01
    ("user123", "wrongpass", "error"),              # LOG-02
    ("nouser", "password123", "error"),             # LOG-03
    ("", "", "error"),                              # LOG-04
    ("' OR 1=1 --", "test", "error")                # LOG-05
])
def test_login(driver, username, password, expected):
    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "password").clear()

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "submit").click()

    time.sleep(1)

    if expected == "dashboard":
        assert "dashboard" in driver.current_url.lower()
    else:
        assert expected in driver.page_source.lower()
