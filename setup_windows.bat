@echo off
echo Setting up Azure Computer Use Model...
echo.

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r computer-use\requirements.txt

REM Create .env file if it doesn't exist
if not exist "computer-use\.env" (
    echo Creating .env file from template...
    copy "computer-use\.env.example" "computer-use\.env" >nul
    echo.
    echo IMPORTANT: Edit computer-use\.env file and add your API key!
    echo.
)

echo.
echo Setup complete!
echo.

REM Test run if user wants
set /p TEST_RUN="Do you want to test the setup now? (Y/N): "
if /i "%TEST_RUN%"=="Y" (
    cd computer-use
    python main.py --instructions "Open notepad and write Hello World"
) else (
    echo To run the application:
    echo   1. cd computer-use
    echo   2. python main.py --instructions "Your task here"
)
echo.
pause