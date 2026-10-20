# 4장 4강 실습 자료

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
# 이 강의의 기본 예제가 읽을 벡터나 검색 결과 파일을 먼저 만들어요.
uv run prepare.py
# 저장한 기본 예제를 위에서 아래로 실행해요. 출력은 교안의 단계별 결과와 비교하세요.
uv run main.py
```

코드를 수정한 뒤 Ctrl+S로 저장하고 uv run main.py로 다시 실행해요.

문서는 교육용 가상 규정이에요. example.invalid 주소 대신 documents.json의 document_id로 원문을 확인하세요.
코드와 입력 자료를 이 강의 폴더에 함께 제공해요. 검수 기록이 있으면 현재 실행 결과와 구분해서 읽어요. uv가 프로젝트 환경과 잠금 파일을 관리하며 수동 환경 활성화는 필요하지 않아요.

## 기본 모델과 선택 비교

기본은 CPU의 E5 small이에요. E5 base는 비교할 때만 다운로드해요.

```powershell
# small과 같은 질문/청크 조건에서 base를 추가로 비교해요. 최초 base 다운로드가 필요해요.
uv run main.py --compare-base
```

recorded_e5_comparison.json은 2026-10-07의 검수 기록이에요. 답이 있는 개발 질문 10개에서 두 모델 모두 Hit@3과 문서 Recall@3이 1.0이었어요. 이 작은 결과로 일반적인 성능 우열을 판단하지 않아요.

## 선택 실습: 외부 임베딩 API 비교

OpenAI 호환 embeddings API와 해당 모델의 사용 권한이 있어야 해요. 현재 교육용 키로 확인한 생성 모델 권한만으로 임베딩 API가 사용 가능하다고 판단하지 않아요. 외부 임베딩 실제 호출은 검증하지 않았어요.

먼저 아래 명령으로 호출 계획만 확인해요. API를 호출하지 않아요.

```powershell
# 입력 수와 요청 계획만 확인해요. --execute가 없으면 외부 API 요청을 보내지 않아요.
uv run compare_api.py
```

사용 가능한 임베딩 모델이 있을 때만 다음을 진행해요. configure_api.py는 이 강의 폴더에 키를 저장하고 화면에 출력하지 않아요.

```powershell
# 이 강의에 필요한 패키지를 프로젝트에 등록하고 설치해요.
uv add openai==2.54.0
# 키를 화면에 표시하지 않고 현재 강의의 .env에 저장해요. 이 명령은 API를 호출하지 않아요.
uv run configure_api.py
$embeddingModel = Read-Host '사용 권한이 있는 임베딩 모델명'
# .env를 읽고 실제 외부 임베딩 비교를 실행해요. 서비스에서 허용한 임베딩 모델명이 필요해요.
uv run --env-file .env compare_api.py --model $embeddingModel --execute
```

문서 28개와 개발 질문 12개를 두 번의 요청으로 임베딩해요. 비용이 발생할 수 있어요. 모델의 일괄 입력 개수와 길이 제한은 서비스에서 확인해요. 이 예제는 일반 텍스트 입력용이며 E5 접두어를 보내지 않아요. 별도 접두어나 입력 유형이 필요한 서비스는 코드 변경 없이 사용하지 않아요.

외부 API에서 문서와 질문을 모두 새로 임베딩하고 api_embedding_comparison.json에 별도 저장해요. 기존 E5 벡터 파일은 변경하지 않아요. 외부 API의 질문 일괄 처리 시간과 E5의 순차 처리 시간은 같은 조건의 속도 비교가 아니에요.
