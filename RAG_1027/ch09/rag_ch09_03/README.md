# 9장 3강 실습 자료

> **rag_day5 묶음으로 받았다면:** 실행 환경은 상위 폴더 `rag_day5`에서 `uv sync` 한 번으로 이미 준비돼요. 아래의 `uv init`, `uv python pin`, `uv add`는 건너뛰고 이 폴더에서 `uv run main.py`부터 실행하세요. 선택 실습(GraphRAG)의 `uv add graphrag…` 대신 `rag_day5/README.md`의 `uv run --with …` 명령을 쓰세요. 자세한 내용은 `rag_day5/README.md`를 보세요.

Windows에서 ZIP을 모두 압축 해제하고 main.py가 있는 폴더를 VS Code로 여세요.
터미널은 PowerShell을 사용해요. 도구 설치는 교안의 실습 준비를 따라 하세요.

```powershell
# 이 강의 폴더의 최초 설정 때만 실행해요. 프로젝트와 Python 버전을 기록해요.
uv init --bare --python 3.12 --no-workspace
uv python pin 3.12
# 이 강의에 필요한 패키지를 프로젝트에 등록하고 설치해요.
uv add networkx==3.7
# uv가 관리하는 프로젝트의 Python 버전을 확인해요. 별도 환경 활성화는 필요 없어요.
uv run python --version
# 저장한 기본 예제를 위에서 아래로 실행해요. 출력은 교안의 단계별 결과와 비교하세요.
uv run main.py
```

코드를 수정한 뒤 Ctrl+S로 저장하고 uv run main.py로 다시 실행해요.

문서는 교육용 가상 규정이에요. example.invalid 주소 대신 documents.json의 document_id로 원문을 확인하세요.
코드와 입력 자료를 이 강의 폴더에 함께 제공해요. 검수 기록이 있으면 현재 실행 결과와 구분해서 읽어요. uv가 프로젝트 환경과 잠금 파일을 관리하며 수동 환경 활성화는 필요하지 않아요.

## 실제 GraphRAG: 로컬 E5와 생성 API 연결

기본 main.py는 NetworkX 탐색과 현행 입력 문서 10개 생성을 수행해요. 실제 GraphRAG는 함께 제공한 graph_local.py로 실행해요. 이 실행 파일이 로컬 E5 제공자를 등록해요.

```powershell
# 이 강의에 필요한 패키지를 프로젝트에 등록하고 설치해요.
uv add graphrag==3.2.0 sentence-transformers==6.0.1 transformers==5.5.2
# 저장한 기본 예제를 위에서 아래로 실행해요. 출력은 교안의 단계별 결과와 비교하세요.
uv run main.py
# GraphRAG의 문서/질문 임베딩 연결을 로컬에서 검사해요. 실제 그래프 색인은 아직 실행하지 않아요.
uv run check_setup.py
```

check_setup.py는 문서 10개와 질문을 CPU E5로 임베딩해요. 생성 API는 호출하지 않아요. document_shape가 [10, 384], query_shape가 [384], long_input_test_passed가 true인지 확인해요. 처음에는 E5 모델 다운로드가 필요해요.

실제 색인과 질의에 사용할 API 키를 이 강의 폴더에서 직접 설정해요.

```powershell
# 키를 화면에 표시하지 않고 현재 강의의 .env에 저장해요. 이 명령은 API를 호출하지 않아요.
uv run configure_api.py
# 실제 GraphRAG 색인을 수행해요. 생성에는 LLM API, 임베딩에는 로컬 E5를 사용해요.
uv run --env-file .env graph_local.py index --root graphrag_demo
# 방금 생성한 색인 파일의 개수와 원문 연결을 확인해요. 의미 정확성은 원문과 별도 대조해요.
uv run inspect_graph.py
# Local: 질문과 관련된 엔티티 주변 근거를 사용해 실제 질의를 실행해요.
uv run --env-file .env graph_local.py query --root graphrag_demo '영수증 제출 규정과 각 승인 조건을 설명해 주세요.' --method local
# Global: 커뮤니티 보고서를 바탕으로 자료 전체의 공통 내용을 질의해요.
uv run --env-file .env graph_local.py query --root graphrag_demo '비용 정산 규정에서 공통으로 요구하는 절차는 무엇인가요?' --method global
# DRIFT: 넓은 맥락에서 시작해 후속 탐색을 수행해요. 여러 LLM 요청이 발생할 수 있어요.
uv run --env-file .env graph_local.py query --root graphrag_demo '비용 정산의 공통 절차와 규정별 예외를 설명해 주세요.' --method drift
```

색인과 질의의 생성 단계는 gpt-6-luna API를 호출하므로 사용량이 발생해요. 임베딩 API는 호출하지 않아요. settings.yaml에 검증한 설정과 프롬프트가 포함돼 있어 graphrag init을 다시 실행하지 않아요. 다른 생성 모델의 권한만 있으면 설정과 응답 형식의 호환성을 먼저 확인해요.

문서와 보고서는 passage: 접두어, 질문은 query: 접두어를 사용해요. 512토큰을 넘을 수 있는 보고서는 480토큰 단위로 나누고 길이 가중 평균 후 다시 정규화해요. 이는 검증용 구현이며 긴 보고서를 한 번에 인코딩한 결과와 같다고 가정하지 않아요.

결과는 graphrag_demo/output에 저장돼요. inspect_graph.py에서 모든 입력 문서의 엔티티, 관계, 커뮤니티 포함 여부를 보고, 금액과 승인 시점은 원문에 대조해요. 숫자와 답변은 실행마다 달라질 수 있어요.

```powershell
# 제공된 이전 검수 기록만 읽어요. 현재 환경에서 모델을 다시 실행한 결과는 아니에요.
uv run show_recorded.py
```

이 명령은 2026-10-07의 실제 검수 기록을 읽어요. 현재 PC에서 새로 색인한 결과는 아니에요. 당시는 엔티티 69개, 관계 62개, 커뮤니티 보고서 17개였고 Local, Global, DRIFT의 세 질문을 대조했어요.

검증 설정은 규정에 맞는 엔티티 유형, use_lcc: false, DRIFT temperature: 1을 사용해요. DRIFT 보고서와 후속 검색 수는 4, 깊이는 1이에요. 이 자료는 모든 질문의 품질이나 대규모 성능을 보장하지 않아요.
