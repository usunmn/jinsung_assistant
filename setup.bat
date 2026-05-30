@echo off
echo === 가상환경 생성 중 ===
python -m venv .venv

echo === 의존성 설치 중 ===
.venv\Scripts\pip install playwright gspread google-auth google-auth-oauthlib

echo === Playwright Chromium 설치 중 ===
.venv\Scripts\python -m playwright install chromium

echo.
echo === 완료 ===
echo.
echo 다음 파일을 이 폴더 루트에 복사하세요:
echo   .google_service_account.json  (구글 서비스 계정 키)
echo.
pause
