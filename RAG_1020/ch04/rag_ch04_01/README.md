# 4장 1강 실습 자료

> **rag_day2 묶음으로 받았다면:** 실행 환경은 상위 폴더 `rag_day2`에서 `uv sync` 한 번으로 이미 준비돼요. 아래의 `uv init`, `uv python pin`, `uv add`는 건너뛰고 이 폴더에서 `uv run`부터 실행하세요. 자세한 내용은 `rag_day2/README.md`를 보세요.

Windows에서 ZIP을 모두 압축 해제하고 main.py가 있는 폴더를 VS Code로 여세요.
터미널은 PowerShell을 사용해요. 도구 설치는 교안의 실습 준비를 따라 하세요.

```powershell
# 이 강의 폴더의 최초 설정 때만 실행해요. 프로젝트와 Python 버전을 기록해요.
uv init --bare --python 3.12 --no-workspace
uv python pin 3.12
# 이 강의에 필요한 패키지를 프로젝트에 등록하고 설치해요.
uv add numpy==2.5.2 sentence-transformers==6.0.1 transformers==5.5.2
# uv가 관리하는 프로젝트의 Python 버전을 확인해요. 별도 환경 활성화는 필요 없어요.
uv run python --version
# 저장한 기본 예제를 위에서 아래로 실행해요. 출력은 교안의 단계별 결과와 비교하세요.
uv run main.py
```

코드를 수정한 뒤 Ctrl+S로 저장하고 uv run main.py로 다시 실행해요.

본문 TODO는 main.py 맨 아래에 작성해요. 정답을 확인하려면 uv run solution.py를 실행해요. 이 명령은 기본 예제도 다시 출력해요.

문서는 교육용 가상 규정이에요. example.invalid 주소 대신 documents.json의 document_id로 원문을 확인하세요.
코드와 입력 자료를 이 강의 폴더에 함께 제공해요. 검수 기록이 있으면 현재 실행 결과와 구분해서 읽어요. uv가 프로젝트 환경과 잠금 파일을 관리하며 수동 환경 활성화는 필요하지 않아요.

## 로컬 E5 준비 확인

기본 모델은 intfloat/multilingual-e5-small이고 CPU에서 실행해요. 첫 실행에는 모델 다운로드가 필요해요. 지정한 공개 모델은 회원가입이나 임베딩 API 키가 필요하지 않아요.

```powershell
# 로컬 E5의 차원과 정규화를 확인해요. 외부 임베딩 API는 호출하지 않아요.
uv run check_embedding.py
```

shape가 [2, 384], normalized와 input_within_limit가 true이면 준비를 확인한 것이에요. 입력은 질문에 query: 접두어, 문서에 passage: 접두어를 붙이고 모델의 512토큰 제한을 확인해요. 이후 main.py를 실행해요. 이 강에서는 main.py가 문서 벡터를 만들어요.
