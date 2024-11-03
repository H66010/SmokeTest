import pytest
import allure
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Inputs.read_csv import read_csv_data
from Pageobject.Login_page_element import LoginPageElement  # PageObjectをインポート
from BaseTestClass import FunctionLibrary  # FunctionLibraryをインポート

# CSVからデータを読み込み（相対パスを使用）
file_path = os.path.join(os.path.dirname(__file__), "../Inputs/Username_and_password.csv")
usernames, passwords = read_csv_data(file_path)

@pytest.fixture(scope="function")
def setup():
    # FunctionLibraryインスタンスを作成してブラウザを初期化
    function_library = FunctionLibrary()
    yield function_library
    function_library.web_quit()

def take_screenshot(driver, name, report_dir):
    """スクリーンショットを撮って保存し、Allureに添付する"""
    screenshot_path = os.path.join(report_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)

@pytest.mark.parametrize("username,password", zip(usernames, passwords))
def test_login(setup, username, password):
    login_page = setup
    report_dir = os.path.join(os.path.dirname(__file__), "../Report")
    os.makedirs(report_dir, exist_ok=True)

    try:
        # ログインページへ移動
        login_page.open_url("https://hotel.testplanisphere.dev/ja/login.html")

        # FunctionLibraryのメソッドを使用してユーザー名とパスワードを入力
        login_page.enter_text(*LoginPageElement.username, username)
        login_page.enter_text(*LoginPageElement.password, password)

        # ログインボタンをクリック
        login_page.click_element(*LoginPageElement.login_button)

        # タイトルが正しいかどうかを確認するまで待機
        expected_title = "マイページ | HOTEL PLANISPHERE - テスト自動化練習サイト"
        WebDriverWait(login_page.driver, 2).until(
            EC.title_is(expected_title)
        )

        # タイトルが正しいか確認
        actual_title = login_page.driver.title
        assert actual_title == expected_title, f"Expected title '{expected_title}', but got '{actual_title}'"

    except AssertionError as e:
        # アサーションエラーの場合にスクリーンショットを撮る
        take_screenshot(login_page.driver, f"AssertionError_{username}", report_dir)
        raise e

    except Exception as e:
        # その他のエラーが発生した場合もスクリーンショットを撮る
        take_screenshot(login_page.driver, f"Exception_{username}", report_dir)
        raise e
