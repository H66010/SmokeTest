from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  # Chromeオプションをインポート
from Driversetup.Init_driver import InitDriver

class FunctionLibrary:
    def __init__(self, driver=None, headless=False):
        if driver is None:
            # InitDriverを使ってブラウザインスタンスを初期化
            self.driver_instance = InitDriver.init_driver()

            # Headlessモードを設定
            if headless:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                self.driver_instance.set_driver("chrome", chrome_options=chrome_options)
            else:
                self.driver_instance.set_driver("chrome")  # 通常モード

            self.driver = self.driver_instance.get_web_driver()
        else:
            self.driver = driver

    def open_url(self, url):
        """URLを開く"""
        self.driver.get(url)

    def click_element(self, by: By, locator: str, timeout: int = 10):
        """ページ上の要素をクリックする"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        element.click()

    def enter_text(self, by: By, locator: str, text: str, timeout: int = 10):
        """テキストフィールドにテキストを入力する"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        element.clear()
        element.send_keys(text)

    def get_element_text(self, by: By, locator: str, timeout: int = 10) -> str:
        """要素のテキストを取得する"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return element.text

    def is_element_visible(self, by: By, locator: str, timeout: int = 10) -> bool:
        """ページ上の要素が表示されているかを確認する"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return element.is_displayed()
        except:
            return False

    def web_quit(self):
        """ブラウザを終了する"""
        if self.driver_instance:
            self.driver_instance.web_quit()
