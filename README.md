# jinsung_assistant

온라인 MD 업무 보조 자동화 도구 모음.

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| naver-store-followers | 경쟁사 네이버 스토어 관심고객수 수집 → 구글 스프레드시트 자동 기입 |

---

## 새 컴퓨터 세팅 방법

### 1. 클론

```
git clone https://github.com/usunmn/jinsung_assistant.git
cd jinsung_assistant
```

### 2. 의존성 설치

```
setup.bat
```

Python 가상환경(`.venv`) 생성 및 필요한 패키지, Playwright Chromium 자동 설치.

### 3. 구글 서비스 계정 키 복사

`.google_service_account.json` 파일을 USB 등으로 받아 프로젝트 루트에 복사.

```
jinsung_assistant/
├── .google_service_account.json  ← 여기
├── .venv/
├── skills/
...
```

> 이 파일은 git에 포함되지 않으므로 컴퓨터마다 수동으로 복사해야 한다.

### 4. Claude Code에 스킬 등록

Claude Code 설정에서 `skills/naver-store-followers` 폴더를 스킬로 등록한다.

---

## 구글 스프레드시트

- 시트명: `날짜별 찜수`
- 인증: 프로젝트 루트의 `.google_service_account.json` (서비스 계정)
- 서비스 계정 이메일: `usunmn@linen-team-441508-t9.iam.gserviceaccount.com`

---

## Python 실행 규칙

모든 Python 실행은 프로젝트 루트의 `.venv`를 사용한다.

```
.venv\Scripts\python <스크립트>
```
