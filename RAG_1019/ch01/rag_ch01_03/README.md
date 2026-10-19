# 1장 3강 실습 자료

> **rag_day1 묶음으로 받았다면:** 실행 환경은 상위 폴더 `rag_day1`에서 `uv sync` 한 번으로 이미 준비돼요. 아래의 `uv init`, `uv python pin`, `uv add`는 건너뛰고 이 폴더에서 `uv run main.py`부터 실행하세요. 자세한 내용은 `rag_day1/README.md`를 보세요.


Windows, VS Code, uv, Python 3.12 기준입니다.
이 폴더에 필요한 코드와 데이터가 모두 있으며 다른 강의 폴더를 참조하지 않습니다.

## 처음 설치하는 경우

1. https://code.visualstudio.com/docs/setup/windows 에서 Windows용 VS Code User Installer를 설치합니다.
2. VS Code 확장 메뉴에서 Microsoft가 배포한 Python 확장을 설치합니다.
3. https://docs.astral.sh/uv/getting-started/installation/ 의 Windows 설치 안내로 uv를 설치합니다.
4. 설치 뒤 VS Code를 완전히 닫았다가 다시 엽니다.

## 강의 프로젝트를 직접 준비하기

ZIP을 모두 압축 풀기 한 뒤, main.py와 documents.json이 들어 있는 rag_ch01_03 폴더를 VS Code의 파일 > 폴더 열기로 엽니다.
터미널 > 새 터미널에서 PowerShell을 선택하고 다음을 순서대로 실행합니다.

```powershell
# uv 명령이 인식되는지 확인하고 수업에서 사용할 Python 3.12를 준비해요.
uv --version
uv python install 3.12
# 이 강의 폴더의 최초 설정 때만 실행해요. 프로젝트와 Python 버전을 기록해요.
uv init --bare --python 3.12 --no-workspace
uv python pin 3.12
# uv가 관리하는 프로젝트의 Python 버전을 확인해요. 별도 환경 활성화는 필요 없어요.
uv run python --version
# 저장한 기본 예제를 위에서 아래로 실행해요. 출력은 교안의 단계별 결과와 비교하세요.
uv run main.py
```

Python 3.12.x가 표시되는지 확인합니다. 설치 상태에 따라 안내 문구는 달라질 수 있습니다.
uv init은 이 폴더의 최초 설정 때 한 번만 실행합니다.
uv가 실행 환경을 자동으로 관리하므로 가상환경을 수동 생성하거나 활성화할 필요가 없습니다.
자료에는 pyproject.toml, .python-version, uv.lock, .venv가 포함되어 있지 않습니다. 위 과정에서 수강생이 직접 생성합니다.

## 코드 읽기와 문제 풀기

main.py는 본문의 기본 예제입니다. 결과를 교안과 비교하며 해당 코드를 읽습니다.
값을 바꾼 뒤 Ctrl+S로 저장하고 uv run main.py로 다시 실행합니다.
TODO 문제는 완성한 뒤 main.py 끝에 추가합니다. 접기 안의 실험과 정답은 별도로 확인합니다.
documents.json의 규정과 주소는 교육용 가상 자료입니다.

## 파일

- main.py: 기본 예제
- documents.json: 이 강의에서 읽는 규정 12개
- README.md: 설정과 실행 안내

- rag_core.py: 이 강의 전용 검색과 생성 함수
- generate_answer.py: 선택 모델 호출 예제

## 선택 실습: Ollama로 답변 생성

기본 실습은 패키지 추가 없이 실행합니다. 아래는 로컬 모델을 호출할 때만 진행합니다.
https://docs.ollama.com/quickstart 를 참고해 Windows용 Ollama를 설치하고 실행합니다.
설치 뒤 VS Code를 다시 열고 이 강의 폴더의 PowerShell에서 실행합니다.

```powershell
# 이 강의에 필요한 패키지를 프로젝트에 등록하고 설치해요.
uv add httpx
# 선택 생성 실습에 사용할 로컬 모델을 내려받아요. 모델 파일은 별도 저장 공간을 사용해요.
ollama pull gemma3:4b-it-q4_K_M
ollama list
# 현재 PowerShell 세션에 서버 주소와 설치된 모델 태그를 지정해요. 새 터미널에서는 다시 설정해요.
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "gemma3:4b-it-q4_K_M"
# 실제 Ollama 생성을 포함해 실행해요. 실행 중인 서버와 설치된 모델 설정이 필요해요.
uv run generate_answer.py
```

이미 모델이 설치되어 있다면 다운로드 단계는 생략할 수 있습니다.
다른 대화 모델을 사용하면 설치된 태그를 OLLAMA_MODEL에 지정합니다.
환경변수 설정과 uv run은 같은 터미널에서 실행합니다.
실제 출력은 모델과 실행 환경에 따라 다릅니다. 상태, 금액, 단위, 조건, 출처를 원문과 대조합니다.

## 자주 막히는 부분

- uv를 찾지 못하면 설치를 확인하고 VS Code를 완전히 재시작합니다.
- pyproject.toml이 이미 있다는 메시지는 초기화를 마쳤다는 뜻일 수 있습니다. 현재 폴더가 맞으면 uv run main.py부터 실행합니다.
- documents.json을 찾지 못하면 압축을 풀었는지, main.py가 있는 폴더를 열었는지 확인합니다.
- 파일을 수정한 뒤에는 저장해야 재실행 결과에 반영됩니다.
