
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ログインページの要素（セレクタ,値）
class LoginPageElement:
    username = (By.ID, "email")
    password = (By.ID, "password")
    login_button = (By.XPATH, '//*[@id="login-button"]')

