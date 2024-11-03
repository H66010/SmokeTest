import subprocess
import os
from datetime import datetime
import argparse

def run_tests_and_generate_report(test_name, headless):
    # 環境変数として headless モードを設定
    os.environ["HEADLESS"] = "true" if headless else "false"
    
    # 現在の時間を取得してフォルダ名に使用
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # レポート保存用のフォルダ名を設定
    report_dir = os.path.join("Report", f"{timestamp}_{test_name}")
    os.makedirs(report_dir, exist_ok=True)
    
    # Pytestを実行してAllure用の結果を保存
    pytest_command = ["pytest", f"Testcases/{test_name}.py", "--alluredir", report_dir]
    try:
        subprocess.run(pytest_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Test execution failed: {e}")
        print("Continuing to generate Allure report...")

    # Allureのレポートを生成
    try:
        generate_command = f"allure generate {report_dir} -o {report_dir}\\allure-report --clean"
        subprocess.run(generate_command, shell=True, check=True)

        # Allureのレポートを非同期で開く
        open_command = f"allure open {report_dir}\\allure-report"
        subprocess.Popen(open_command, shell=True)  # 非同期で実行
    except subprocess.CalledProcessError as e:
        print(f"Error generating or opening Allure report: {e}")
        print("Please ensure Allure is installed correctly and the path is set.")

if __name__ == "__main__":
    # コマンドライン引数を解析
    parser = argparse.ArgumentParser(description="Run selected test and generate Allure report.")
    parser.add_argument(
        "test_name",
        type=str,
        help="The name of the test file to run (without .py extension, e.g., Test_Login)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run tests in headless mode"
    )
    
    args = parser.parse_args()
    run_tests_and_generate_report(args.test_name, args.headless)
