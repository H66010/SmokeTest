import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# ブラウザドライバの初期化と管理を行うクラス
class InitDriver:
    driver = None  # クラス変数として唯一のドライバインスタンスを保持

    def __init__(self):
        self.web_driver = None  # インスタンスごとのWebDriver保持用
        self.timeout_sec = 20  # WebDriverの操作タイムアウト時間（秒）

    @classmethod
    def init_driver(cls):
        """
        Singletonパターンで唯一のInitDriverインスタンスを返す。
        まだ存在しない場合は新規作成し、それを返す。
        """
        if cls.driver is None:
            cls.driver = InitDriver()  # 初回時に唯一のインスタンスを生成
        return cls.driver

    def set_driver(self, browser):
        """
        指定されたブラウザに基づき、WebDriverのインスタンスを生成し設定する。
        
        Args:
            browser (str): 使用するブラウザを指定（"chrome" または "firefox"）
        """
        # 環境変数"HEADLESS"の設定に応じてヘッドレスモードを有効化
        headless = os.environ.get("HEADLESS") == "true"
        
        # Chromeブラウザの場合の設定
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")  # ヘッドレスモードで起動
                options.add_argument("--disable-gpu")  # GPU無効化（ヘッドレス環境の互換性確保）
                options.add_argument("--window-size=1920,1080")  # 表示領域の固定
                options.add_argument("--no-sandbox")  # サンドボックス無効化（Linux環境用）
                options.add_argument("--disable-dev-shm-usage")  # 共有メモリ領域の無効化
            # ChromeDriverのインスタンスを作成し、self.web_driverに保持
            self.web_driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=options
            )

        # Firefoxブラウザの場合の設定
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")  # ヘッドレスモードで起動
                options.add_argument("--window-size=1920,1080")  # 表示領域の固定
            # FirefoxDriverのインスタンスを作成し、self.web_driverに保持
            self.web_driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()), options=options
            )

        else:
            # 指定が不正な場合のエラーメッセージ
            print("Please specify a valid WebDriver ('chrome' or 'firefox').")

    def get_web_driver(self):
        """
        設定済みのWebDriverインスタンスを返す。
        
        Returns:
            WebDriver: 設定されたWebDriverインスタンス
        """
        return self.web_driver

    def web_quit(self):
        """
        WebDriverを終了し、リソースを解放する。
        """
        if self.web_driver:
            self.web_driver.quit()  # ドライバの終了とプロセスの解放
