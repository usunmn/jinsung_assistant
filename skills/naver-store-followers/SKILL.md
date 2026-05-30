---
name: naver-store-followers
description: 네이버 스마트스토어 또는 브랜드스토어의 관심고객수를 Playwright로 수집하고 구글 스프레드시트에 자동 기입하는 스킬. 사용자가 "관심고객수", "관심수 수집", "관심 고객", "스토어 팔로워", "경쟁사 관심고객" 등을 언급하거나 네이버 스토어 URL 목록을 주면서 수집/비교를 요청할 때 반드시 이 스킬을 사용할 것. smartstore.naver.com과 brand.naver.com 둘 다 지원.
---

# 네이버 스토어 관심고객수 수집 스킬

## 개요

Playwright headless Chromium으로 관심고객수를 수집하고, 구글 스프레드시트(날짜별 찜수 시트)에 자동 기입한다.

## 저장된 스토어 목록

메모리(`naver-stores.md`)에 저장된 9개 스토어를 기본으로 사용한다:

| 이름 | URL |
|------|-----|
| 맛딜 | https://smartstore.naver.com/haedeunfarm |
| 대한민국농수산 | https://brand.naver.com/koreasusan1 |
| 땡큐파머스 | https://brand.naver.com/thankyoufarmers |
| 과일꾼 | https://brand.naver.com/fruitggun |
| 맛군 | https://brand.naver.com/mggfood |
| 백년밥상 | https://brand.naver.com/goodfoods |
| 산지도매센타 | https://brand.naver.com/santafarmer |
| 픽미푸드 | https://brand.naver.com/pickmefood |
| 돌쇠네 | https://smartstore.naver.com/dolfarmers |

## 실행 순서

### 1단계: 관심고객수 수집

```bash
python <skill_dir>/scripts/scrape_followers.py \
  --urls "https://smartstore.naver.com/haedeunfarm" "https://brand.naver.com/koreasusan1" "https://brand.naver.com/thankyoufarmers" "https://brand.naver.com/fruitggun" "https://brand.naver.com/mggfood" "https://brand.naver.com/goodfoods" "https://brand.naver.com/santafarmer" "https://brand.naver.com/pickmefood" "https://smartstore.naver.com/dolfarmers" \
  --names "맛딜" "대한민국농수산" "땡큐파머스" "과일꾼" "맛군" "백년밥상" "산지도매센타" "픽미푸드" "돌쇠네"
```

### 2단계: 스프레드시트 기입

수집 결과에서 각 스토어의 관심고객수를 **맛딜 대한민국농수산 땡큐파머스 과일꾼 맛군 백년밥상 산지도매센타 픽미푸드 돌쇠네 순서**로 추출해 아래 스크립트에 전달한다.

```bash
python <skill_dir>/scripts/update_sheet.py \
  --counts <맛딜> <대한민국농수산> <땡큐파머스> <과일꾼> <맛군> <백년밥상> <산지도매센타> <픽미푸드> <돌쇠네>
```

- 오늘 날짜 행을 자동으로 찾아 기입한다
- 이미 데이터가 있으면 덮어쓴다
- 증감 컬럼은 시트에 수식이 있으므로 건드리지 않는다
- 숫자 서식(`#,##0`)을 자동 적용한다

`<skill_dir>`는 이 SKILL.md가 위치한 디렉토리 경로로 치환할 것.

## 스프레드시트 정보

- ID: `162mZfqbm-5goHCQkdjvWd4zQpTARTdfiO96o2D5T_vs`
- 시트명: `날짜별 찜수`
- 인증: `~/.google_service_account.json` (서비스 계정)

## 쿠키 자동 처리

scrape_followers.py가 아래 순서로 쿠키를 자동 탐색한다:
1. 환경변수 `NAVER_NID_AUT`, `NAVER_NID_SES`
2. `~/.naver_cookies.json` 파일
3. Chrome 프로필 자동 추출 (Chrome이 닫혀 있을 때)

## 출력 형식

```
| 순위 | 스토어 | 관심고객수 |
|------|--------|----------:|
| 1 | 대한민국농수산 | 1,255,145 |
| 2 | 땡큐파머스 | 688,119 |
...
```

## 오류 처리

| 상황 | 대응 |
|------|------|
| 쿠키 없음 | 자동 추출 시도 → 실패 시 DevTools 안내 |
| 관심고객수 추출 실패 | 해당 스토어 "추출 실패"로 표시 후 계속 |
| Playwright 미설치 | `pip install playwright && python -m playwright install chromium` 안내 |
| 서비스 계정 파일 없음 | `~/.google_service_account.json` 경로 안내 |
