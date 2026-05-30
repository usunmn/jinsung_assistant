# jinsung_assistant

## 프로젝트 목적

온라인 MD 업무를 보조하는 자동화 도구 모음이다.
경쟁사 스토어 관심고객수 수집, 구글 스프레드시트 기입 등 반복 업무를 Claude Code 스킬로 자동화한다.

## 가상환경

이 프로젝트의 모든 Python 실행은 `.venv`를 사용한다.

- 인터프리터: `.venv/Scripts/python` (Windows)
- 스크립트 실행 시 `python` 대신 `.venv/Scripts/python` 또는 `.venv\Scripts\python`을 사용할 것
- 패키지 설치 시 `.venv/Scripts/pip install` 사용

**`.venv` 폴더가 없으면 Python 스크립트 실행 전에 `setup.bat`을 먼저 실행한다.**

## 인증 파일

- `.google_service_account.json` — 구글 스프레드시트 서비스 계정 키. 이 파일은 git에 포함되지 않으며 각 컴퓨터에 수동으로 복사해야 한다.
