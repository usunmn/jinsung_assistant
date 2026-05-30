# -*- coding: utf-8 -*-
"""
Chrome에서 네이버 쿠키(NID_AUT, NID_SES)를 자동으로 추출하는 스크립트.
Windows 전용.

동작:
  - Chrome이 닫혀 있으면 Playwright로 프로필을 열어 쿠키 자동 추출
  - Chrome이 실행 중이면 DevTools 복사 방법 안내

사용법:
  python get_chrome_cookies.py           # 콘솔 출력
  python get_chrome_cookies.py --save    # ~/.naver_cookies.json에 저장
"""

import io, json, os, subprocess, sys, time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

CHROME_PROFILE_DIR = Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data"
NAVER_COOKIE_FILE = Path.home() / ".naver_cookies.json"


def is_chrome_running():
    try:
        r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq chrome.exe", "/NH"],
                           capture_output=True, text=True, timeout=5)
        return "chrome.exe" in r.stdout
    except Exception:
        return False


def fetch_via_playwright(profile="Default"):
    """Chrome이 닫혀 있을 때 Playwright로 프로필을 직접 열어 쿠키 추출"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("playwright 미설치: pip install playwright && python -m playwright install chromium")

    user_data_dir = str(CHROME_PROFILE_DIR / profile)
    cookies = {}

    with sync_playwright() as p:
        try:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir, channel="chrome", headless=True,
                args=["--no-first-run", "--disable-extensions"],
            )
        except Exception:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir, headless=True,
                args=["--no-first-run"],
            )

        page = ctx.new_page()
        page.goto("https://www.naver.com", wait_until="domcontentloaded", timeout=20000)
        time.sleep(2)

        for c in ctx.cookies("https://www.naver.com"):
            if c["name"] in ("NID_AUT", "NID_SES"):
                cookies[c["name"]] = c["value"]

        ctx.close()

    return cookies


def print_devtools_guide():
    print()
    print("=" * 60)
    print("  Chrome이 실행 중이라 자동 추출이 불가합니다.")
    print("  아래 방법으로 쿠키를 1회만 복사해주세요:")
    print("=" * 60)
    print()
    print("  1. Chrome에서 naver.com을 로그인한 상태로 엽니다")
    print("  2. F12 → Application 탭 클릭")
    print("  3. 왼쪽에서 Cookies → https://www.naver.com 클릭")
    print("  4. 'NID_AUT' 행 → Value 열 값을 복사")
    print("  5. 'NID_SES' 행 → Value 열 값을 복사")
    print()
    print("  복사 후 ~/.naver_cookies.json 파일을 만드세요:")
    print()
    print('  {')
    print('    "NID_AUT": "복사한_NID_AUT_값",')
    print('    "NID_SES": "복사한_NID_SES_값"')
    print('  }')
    print()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--profile", default="Default")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if is_chrome_running() and not args.force:
        print("[자동 추출 불가] Chrome이 실행 중입니다.")
        print_devtools_guide()
        sys.exit(1)

    print("Chrome 프로필에서 네이버 쿠키를 읽는 중...")
    try:
        cookies = fetch_via_playwright(args.profile)
    except Exception as e:
        print(f"오류: {e}")
        print_devtools_guide()
        sys.exit(1)

    if not cookies.get("NID_AUT") or not cookies.get("NID_SES"):
        print("오류: NID_AUT 또는 NID_SES를 찾을 수 없습니다. 네이버에 Chrome으로 로그인하세요.")
        sys.exit(1)

    print(f"NID_AUT: {cookies['NID_AUT'][:25]}...")
    print(f"NID_SES: {cookies['NID_SES'][:25]}...")

    if args.save:
        NAVER_COOKIE_FILE.write_text(json.dumps(cookies, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n저장 완료: {NAVER_COOKIE_FILE}")
    else:
        print("\n--save 옵션을 추가하면 ~/.naver_cookies.json에 자동 저장됩니다.")


if __name__ == "__main__":
    main()
