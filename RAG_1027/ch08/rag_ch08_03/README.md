# 8장 3강 실습 자료

> **rag_day5 묶음으로 받았다면:** 실행 환경은 상위 폴더 `rag_day5`에서 `uv sync` 한 번으로 이미 준비돼요. 아래의 `uv init`, `uv python pin`, `uv add`는 건너뛰고 이 폴더에서 `uv run main.py`부터 실행하세요. 선택 실습(RAGAS)의 `uv add ragas…` 대신 `rag_day5/README.md`의 `uv run --with …` 명령을 쓰세요. 자세한 내용은 `rag_day5/README.md`를 보세요.

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

문서는 교육용 가상 규정이에요. example.invalid 주소 대신 documents.json의 document_id로 원문을 확인하세요.
코드와 입력 자료를 이 강의 폴더에 함께 제공해요. 검수 기록이 있으면 현재 실행 결과와 구분해서 읽어요. uv가 프로젝트 환경과 잠금 파일을 관리하며 수동 환경 활성화는 필요하지 않아요.

## 실제 RAGAS 평가: 로컬 E5 사용

기본 main.py는 검색 Context와 사람이 작성한 답변 A, B, C를 answer_review_08.json에 저장해요. 실제 평가는 run_ragas.py로 실행해요.

```powershell
# 이 강의에 필요한 패키지를 프로젝트에 등록하고 설치해요.
uv add ragas==0.4.3 openai==2.54.0 langchain-community==0.3.31 sentence-transformers==6.0.1 transformers==5.5.2
# 저장한 기본 예제를 위에서 아래로 실행해요. 출력은 교안의 단계별 결과와 비교하세요.
uv run main.py
# 로컬 E5와 지표 구성을 검사하는 준비 모드예요. 평가 LLM은 호출하지 않아요.
uv run run_ragas.py
```

마지막 명령은 로컬 E5와 네 지표의 준비 상태를 확인하며 평가 API를 호출하지 않아요. 첫 실행에는 공개 E5 모델을 다운로드해요. local_embedding_check의 shape가 [2, 384], generation_requests가 0인지 확인해요.

평가 모델 API를 사용할 권한과 사용 한도가 있으면 키를 직접 설정해요. 현재 검수한 모델은 gpt-6-luna예요. gpt-5.6-luna 선택은 허용하지만 이 실습의 실제 점수 검증 모델은 gpt-6-luna예요.

```powershell
# 키를 화면에 표시하지 않고 현재 강의의 .env에 저장해요. 이 명령은 API를 호출하지 않아요.
uv run configure_api.py
# 실제 RAGAS 평가 LLM 요청을 보내요. 임베딩은 로컬 E5로 계산해요.
uv run --env-file .env run_ragas.py --model gpt-6-luna --execute
```

이 명령은 유료 평가 모델을 호출해요. 최대 요청은 20회로 제한하며 임베딩은 CPU의 로컬 E5가 계산해요. 기본 API 주소는 api.openai.com이고 별도 게이트웨이는 이 제한된 검증 코드에 바로 연결할 수 없어요. 키는 .env에만 저장하고 배포나 제출에 포함하지 않아요.

RAGAS의 질문 유사도 비교에서는 원질문과 생성된 질문 양쪽에 query: 접두어를 사용해요. 임베딩 모델과 접두어를 바꾸면 점수 기준도 바뀌므로 같은 설정끼리 비교해요. 실제 점수는 ragas_local_result.json에 저장돼요.

```powershell
# 제공된 이전 검수 기록만 읽어요. 현재 환경에서 모델을 다시 실행한 결과는 아니에요.
uv run run_ragas.py --show-recorded
```

이 명령은 2026-10-07의 이전 검수 기록을 읽어요. 유료 API를 호출하지 않으며 현재 수강생이 직접 평가한 결과로 제출하지 않아요. Context Precision은 검색 순서에 따른 평균 정밀도이므로 1.0이어도 모든 Context가 유용하다는 뜻은 아니에요.
