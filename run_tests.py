import subprocess
import os
from datetime import datetime
import argparse

def run_tests_and_generate_report(test_name, headless):
    """
    指定されたテストを実行し、Allureでレポートを生成・表示する。
    
    Args:
        test_name (str): 実行するテストファイル名（拡張子なし）
        headless (bool): ヘッドレスモードでテストを実行するかどうか
    """
    # ヘッドレスモードの環境変数を設定
    os.environ["HEADLESS"] = "true" if headless else "false"
    
    # 実行時のタイムスタンプを取得してフォルダ名に使用
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # レポート保存用ディレクトリを作成
    report_dir = os.path.join("Report", f"{timestamp}_{test_name}")
    os.makedirs(report_dir, exist_ok=True)
    
    # Pytestを実行し、結果をAllureのフォーマットで保存
    pytest_command = ["pytest", f"Testcases/{test_name}.py", "--alluredir", report_dir]
    try:
        subprocess.run(pytest_command, check=True)
    except subprocess.CalledProcessError as e:
        # テスト実行に失敗した場合のエラーメッセージ出力
        print(f"Test execution failed: {e}")
        print("Continuing to generate Allure report...")

    # Allureのレポートを生成
    try:
        generate_command = f"allure generate {report_dir} -o {report_dir}\\allure-report --clean"
        subprocess.run(generate_command, shell=True, check=True)

        # 非同期でAllureレポートを開く
        open_command = f"allure open {report_dir}\\allure-report"
        subprocess.Popen(open_command, shell=True)
    except subprocess.CalledProcessError as e:
        # Allureレポート生成または表示に失敗した場合のエラーメッセージ出力
        print(f"Error generating or opening Allure report: {e}")
        print("Please ensure Allure is installed correctly and the path is set.")

if __name__ == "__main__":
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="Run selected test and generate Allure report.")
    parser.add_argument(
        "test_name",
        type=str,
        help="実行するテストファイル名（.py拡張子は不要、例：Test_Login）"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="ヘッドレスモードでテストを実行"
    )
    
    # コマンドライン引数を関数に渡して実行
    args = parser.parse_args()
    run_tests_and_generate_report(args.test_name, args.headless)
