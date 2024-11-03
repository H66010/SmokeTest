@echo off

:: 仮想環境を構築
echo Creating virtual environment...
python -m venv venv

:: 仮想環境をアクティブ化
echo Activating virtual environment...
call venv\Scripts\activate

:: 必要なパッケージをインストール
echo Installing dependencies...

:: setup.py を使用して依存関係をインストール
echo Installing dependencies from setup.py...
pip install . --use-feature=in-tree-build

:: 自作モジュールを編集モードでインストール
echo Installing custom module in editable mode...
pip install -e .

:menu
cls
echo.
echo Please select the tests you want to run:
echo 1. Test_Login
echo 2. Test_AnotherTest
echo 3. Test_SomeOtherTest
echo 4. TestAll (Run all tests)
echo 5. Exit
echo.
set /p test_choices="Enter the numbers of the tests you want to run, separated by spaces (e.g., 1 2 3), or 5 to exit: "

:: Exit オプションのチェック
if "%test_choices%"=="5" goto end

:: Headless モードの指定
echo.
set /p headless_mode="Do you want to run the tests in Headless mode? (Y/N): "

:: Headless モードの設定
set headless_flag=
if /I "%headless_mode%"=="Y" set headless_flag=--headless

:: 選択されたテストを解析して実行
set test_list=
for %%i in (%test_choices%) do (
    if "%%i"=="1" set test_list=%test_list% Test_Login
    if "%%i"=="2" set test_list=%test_list% Test_AnotherTest
    if "%%i"=="3" set test_list=%test_list% Test_SomeOtherTest
    if "%%i"=="4" (
        set test_list=Test_Login Test_AnotherTest Test_SomeOtherTest
        goto run_tests
    )
)

:run_tests
:: 各テストを連続して実行
for %%t in (%test_list%) do (
    echo Running %%t with headless_flag: %headless_flag%...
    python run_tests.py %%t %headless_flag%
)

:: 終了後メニューに戻る
goto menu

:end
:: 仮想環境を終了する
echo Deactivating virtual environment...
deactivate

:: バッチファイルの終了
pause
