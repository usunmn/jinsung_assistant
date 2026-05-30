@echo off
echo === 의존성 설치 중 ===
pip install playwright gspread google-auth google-auth-oauthlib
python -m playwright install chromium
echo.
echo === 완료 ===
echo.
echo 다음 파일을 수동으로 복사하세요:
echo   ~/.google_service_account.json  (구글 서비스 계정 키)
echo.
pause
