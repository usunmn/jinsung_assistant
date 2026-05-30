# -*- coding: utf-8 -*-
"""
네이버 스토어 관심고객수를 구글 스프레드시트에 기입
사용법: python update_sheet.py --counts 11901 1255145 688119 678107 568679 326866 272107 87452 24788
       (맛딜 대한민국농수산 땡큐파머스 과일꾼 맛군 백년밥상 산지도매센타 픽미푸드 돌쇠네 순서)
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse
from datetime import date
from pathlib import Path



SPREADSHEET_ID = "162mZfqbm-5goHCQkdjvWd4zQpTARTdfiO96o2D5T_vs"
SHEET_NAME = "날짜별 찜수"
SERVICE_ACCOUNT_PATH = Path(__file__).resolve().parent.parent.parent.parent / ".google_service_account.json"

STORE_NAMES = ["맛딜", "대한민국농수산", "땡큐파머스", "과일꾼", "맛군", "백년밥상", "산지도매센타", "픽미푸드", "돌쇠네"]
WEEKDAYS_KR = ["월", "화", "수", "목", "금", "토", "일"]

# 시트 컬럼 구조 (0-based index)
# col 0: (빈 열)
# col 1: 날짜
# col 2: 맛딜, col 3: 맛딜변화
# col 4: 대한민국농수산, col 5: 변화
# col 6: 땡큐파머스, col 7: 변화
# col 8: 과일꾼, col 9: 변화
# col 10: 맛군, col 11: 변화
# col 12: 백년밥상, col 13: 변화
# col 14: 산지도매센타, col 15: 변화
# col 16: 픽미푸드, col 17: 변화
# col 18: 돌쇠네, col 19: 변화
DATE_COL = 1       # 0-based
DATA_START_COL = 2 # 0-based, 첫 번째 관심고객수 컬럼

def fmt_date(d: date) -> str:
    return f"{d.strftime('%Y-%m-%d')} ({WEEKDAYS_KR[d.weekday()]})"

def get_sheet():
    import gspread
    from google.oauth2.service_account import Credentials

    if not SERVICE_ACCOUNT_PATH.exists():
        print(f"\n오류: {SERVICE_ACCOUNT_PATH} 파일이 없습니다.")
        sys.exit(1)

    creds = Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_PATH),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

def find_today_row(all_vals: list, today_str: str):
    """오늘 날짜 행 인덱스(0-based) 반환. 없으면 None."""
    for i, row in enumerate(all_vals):
        if len(row) > DATE_COL and row[DATE_COL].strip() == today_str:
            return i
    return None

def col_letter(n: int) -> str:
    """0-based 컬럼 인덱스를 A, B, ..., Z, AA 형식으로 변환"""
    n += 1  # 1-based
    result = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        result = chr(65 + r) + result
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--counts", nargs="+", type=int, required=True)
    args = p.parse_args()

    if len(args.counts) != len(STORE_NAMES):
        print(f"오류: {len(STORE_NAMES)}개 값 필요 (현재 {len(args.counts)}개)")
        sys.exit(1)

    today_str = fmt_date(date.today())
    print(f"대상 날짜: {today_str}")

    ws = get_sheet()
    all_vals = ws.get_all_values()

    row_idx = find_today_row(all_vals, today_str)
    if row_idx is None:
        print(f"오류: 시트에서 '{today_str}' 행을 찾을 수 없습니다.")
        sys.exit(1)

    row_num = row_idx + 1  # 1-based (gspread)

    # 관심고객수 컬럼만 업데이트 (증감 컬럼은 수식이 있으므로 건드리지 않음)
    updates = []
    for i, count in enumerate(args.counts):
        col = DATA_START_COL + i * 2  # 0-based: 2, 4, 6, ...
        cell = col_letter(col) + str(row_num)
        updates.append({"range": cell, "values": [[count]]})

    ws.batch_update(updates)

    # 값을 쓴 셀에 숫자 서식 적용 (기존 행과 동일하게)
    fmt_ranges = []
    for i in range(len(STORE_NAMES)):
        col = DATA_START_COL + i * 2
        cell = col_letter(col) + str(row_num)
        fmt_ranges.append(cell)
    ws.format(fmt_ranges, {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})

    print(f"\n스프레드시트 업데이트 완료 ({today_str}, row {row_num})")
    for i, name in enumerate(STORE_NAMES):
        print(f"  {name}: {args.counts[i]:,}")

if __name__ == "__main__":
    main()
