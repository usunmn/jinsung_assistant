# -*- coding: utf-8 -*-
"""
네이버 스마트스토어/브랜드스토어 관심고객수 수집 스크립트
사용법: python scrape_followers.py --urls URL1 URL2 ... [--names NAME1 NAME2 ...]
"""

import io, json, os, re, subprocess, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def load_cookies():
    """쿠키를 환경변수 → 파일 → Chrome 자동 추출 순서로 탐색"""
    nid_aut = os.environ.get("NAVER_NID_AUT")
    nid_ses = os.environ.get("NAVER_NID_SES")
    if nid_aut and nid_ses:
        return nid_aut, nid_ses

    config_path = Path.home() / ".naver_cookies.json"
    if config_path.exists():
        data = json.loads(config_path.read_text(encoding="utf-8"))
        nid_aut, nid_ses = data.get("NID_AUT"), data.get("NID_SES")
        if nid_aut and nid_ses:
            return nid_aut, nid_ses

    # Chrome 프로필 자동 추출 시도
    get_cookies = Path(__file__).parent / "get_chrome_cookies.py"
    if get_cookies.exists():
        print("저장된 쿠키 없음. Chrome 프로필에서 자동 추출 시도 중...", flush=True)
        result = subprocess.run(
            [sys.executable, str(get_cookies), "--save"],
            capture_output=True, timeout=60,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        stdout = result.stdout.decode("utf-8", errors="replace")
        if result.returncode == 0 and config_path.exists():
            data = json.loads(config_path.read_text(encoding="utf-8"))
            nid_aut, nid_ses = data.get("NID_AUT"), data.get("NID_SES")
            if nid_aut and nid_ses:
                print("쿠키 자동 추출 성공!", flush=True)
                return nid_aut, nid_ses
        if stdout:
            print(stdout, flush=True)

    return None, None


def extract_store_id(url):
    m = re.search(r"naver\.com/([^/?#]+)", url)
    return m.group(1) if m else url


def scrape_followers(urls, names, nid_aut, nid_ses):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("오류: playwright 미설치. pip install playwright && python -m playwright install chromium")
        sys.exit(1)

    cookies = [
        {"name": "NID_AUT", "value": nid_aut, "domain": ".naver.com", "path": "/"},
        {"name": "NID_SES", "value": nid_ses, "domain": ".naver.com", "path": "/"},
    ]
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for i, url in enumerate(urls):
            name = names[i] if i < len(names) else extract_store_id(url)
            ctx = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
                locale="ko-KR",
            )
            ctx.add_cookies(cookies)
            page = ctx.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                text = page.inner_text("body")
                m = re.search(r"관심고객수\s*([\d,]+)", text)
                if m:
                    count_str = m.group(1)
                    results.append({"name": name, "url": url, "count": int(count_str.replace(",", "")), "count_str": count_str})
                    print(f"  [OK] {name}: {count_str}명", flush=True)
                else:
                    results.append({"name": name, "url": url, "count": -1, "count_str": "추출 실패"})
                    print(f"  [실패] {name}: 관심고객수를 찾을 수 없음", flush=True)
            except Exception as e:
                results.append({"name": name, "url": url, "count": -1, "count_str": f"오류: {e}"})
                print(f"  [오류] {name}: {e}", flush=True)
            finally:
                ctx.close()
        browser.close()

    return results


def print_table(results):
    sorted_r = sorted(results, key=lambda x: x["count"], reverse=True)
    print("\n## 관심고객수 순위\n")
    print("| 순위 | 스토어 | 관심고객수 |")
    print("|------|--------|----------:|")
    rank = 1
    for r in sorted_r:
        if r["count"] >= 0:
            print(f"| {rank} | {r['name']} | **{r['count_str']}** |")
            rank += 1
    for r in [x for x in results if x["count"] < 0]:
        print(f"- {r['name']}: {r['count_str']}")


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--urls", nargs="+", required=True)
    p.add_argument("--names", nargs="+", default=[])
    args = p.parse_args()

    nid_aut, nid_ses = load_cookies()
    if not nid_aut or not nid_ses:
        print("\n쿠키를 찾을 수 없습니다. Chrome을 닫고 다시 실행하거나 ~/.naver_cookies.json을 만들어주세요.")
        sys.exit(1)

    print(f"수집 시작: {len(args.urls)}개 스토어\n")
    results = scrape_followers(args.urls, args.names, nid_aut, nid_ses)
    print_table(results)


if __name__ == "__main__":
    main()
