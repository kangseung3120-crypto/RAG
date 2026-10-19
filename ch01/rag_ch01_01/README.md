# 1장 1강 실습 자료

> **rag_day1 묶음으로 받았다면:** 실행 환경은 상위 폴더 `rag_day1`에서 `uv sync` 한 번으로 이미 준비돼요. 아래의 `uv init`, `uv python pin`, `uv add`는 건너뛰고 이 폴더에서 `uv run main.py`부터 실행하세요. 자세한 내용은 `rag_day1/README.md`를 보세요.


Windows, VS Code, uv, Python 3.12 기준입니다.
이 폴더에 필요한 코드와 데이터가 모두 있으며 다른 강의 폴더를 참조하지 않습니다.

## 처음 설치하는 경우

1. https://code.visualstudio.com/docs/setup/windows 에서 Windows용 VS Code User Installer를 설치합니다.
2. VS Code 확장 메뉴에서 Microsoft가 배포한 Python 확장을 설치합니다.
3. https://docs.astral.sh/uv/getting-started/installation/ 의 Windows 설치 안내로 uv를 설치합니다.
4. 설치 뒤 VS Code를 완전히 닫았다가 다시 엽니다.

## 강의 프로젝트를 직접 준비하기

ZIP을 모두 압축 풀기 한 뒤, main.py와 documents.json이 들어 있는 rag_ch01_01 폴더를 VS Code의 파일 > 폴더 열기로 엽니다.
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

## 자주 막히는 부분

- uv를 찾지 못하면 설치를 확인하고 VS Code를 완전히 재시작합니다.
- pyproject.toml이 이미 있다는 메시지는 초기화를 마쳤다는 뜻일 수 있습니다. 현재 폴더가 맞으면 uv run main.py부터 실행합니다.
- documents.json을 찾지 못하면 압축을 풀었는지, main.py가 있는 폴더를 열었는지 확인합니다.
- 파일을 수정한 뒤에는 저장해야 재실행 결과에 반영됩니다.
