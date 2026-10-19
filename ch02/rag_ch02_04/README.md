# 2장 4강 실습 자료

> **rag_day1 묶음으로 받았다면:** 실행 환경은 상위 폴더 `rag_day1`에서 `uv sync` 한 번으로 이미 준비돼요. 아래의 `uv init`, `uv python pin`, `uv add`는 건너뛰고 이 폴더에서 `uv run main.py`부터 실행하세요. 자세한 내용은 `rag_day1/README.md`를 보세요.


Windows에서 ZIP을 모두 압축 해제하고 main.py가 있는 폴더를 VS Code로 여세요.
터미널은 PowerShell을 사용해요. 도구 설치는 교안의 실습 준비를 따라 하세요.

```powershell
# 이 강의 폴더의 최초 설정 때만 실행해요. 프로젝트와 Python 버전을 기록해요.
uv init --bare --python 3.12 --no-workspace
uv python pin 3.12
# uv가 관리하는 프로젝트의 Python 버전을 확인해요. 별도 환경 활성화는 필요 없어요.
uv run python --version
# 저장한 기본 예제를 위에서 아래로 실행해요. 출력은 교안의 단계별 결과와 비교하세요.
uv run main.py
```

코드를 수정한 뒤 Ctrl+S로 저장하고 uv run main.py로 다시 실행해요.

본문 TODO는 main.py 맨 아래에 작성해요. 정답을 확인하려면 uv run solution.py를 실행해요. 이 명령은 기본 예제도 다시 출력해요.

문서는 교육용 가상 규정이에요. example.invalid 주소 대신 documents.json의 document_id로 원문을 확인하세요.
이 폴더에는 원본 입력만 제공해요. uv가 프로젝트 환경과 잠금 파일을 관리하며 수동 환경 활성화는 필요하지 않아요.
