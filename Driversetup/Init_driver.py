import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class InitDriver:
    driver = None

    def __init__(self):
        self.web_driver = None
        self.timeout_sec = 20

    @classmethod
    def init_driver(cls):
        if cls.driver is None:
            cls.driver = InitDriver()
        return cls.driver

    def set_driver(self, browser):
        headless = os.environ.get("HEADLESS") == "true"
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
            self.web_driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=options
            )
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
            self.web_driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()), options=options
            )
        else:
            print("Please specify a valid WebDriver ('chrome' or 'firefox').")

    def get_web_driver(self):
        return self.web_driver

    def web_quit(self):
        if self.web_driver:
            self.web_driver.quit()
