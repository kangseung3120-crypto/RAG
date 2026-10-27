# RAG 5일차 실습 자료 (8장 오전 · 9장 오후)

8장과 9장 강의 8개의 실습 폴더를 하나로 묶었어요. **uv 실행 환경은 이 폴더에 하나만 만들고 8개 강의가 함께 써요.** 그래서 오늘은 처음에 한 번만 세팅하면 돼요.

## 폴더 구성

```
rag_day5/
├─ pyproject.toml      ← 8개 강의에 필요한 패키지 목록 (함께 씀)
├─ uv.lock             ← 패키지 버전 고정 (함께 씀)
├─ .python-version     ← Python 3.12 (함께 씀)
├─ ch08/  (오전)
│  ├─ rag_ch08_01/     8장 1강  소규모 Golden Dataset 설계
│  ├─ rag_ch08_02/     8장 2강  검색 평가: Hit@k / Recall@k
│  ├─ rag_ch08_03/     8장 3강  답변 평가: RAGAS 기본 지표
│  └─ rag_ch08_04/     8장 4강  오류 분류와 개선 전후 비교
└─ ch09/  (오후)
   ├─ rag_ch09_01/     9장 1강  Parent-Child와 Context Compression
   ├─ rag_ch09_02/     9장 2강  Corrective / Agentic RAG
   ├─ rag_ch09_03/     9장 3강  GraphRAG Local / Global / DRIFT
   └─ rag_ch09_04/     9장 4강  Multimodal RAG와 ColPali
```

강의 폴더 안의 파일은 노션 교안의 ZIP과 같아요. 여기에 퀴즈 파일 3개(`q_easy.py`, `q_hard.py`, `q_solution.py`)를 더했어요.

## 처음 한 번만: 세팅

1. **압축 풀기:** ZIP을 OneDrive와 동기화되지 않는 **짧은 경로**(예: `C:\rag`)에 풀어요. 바탕 화면이나 문서 폴더가 OneDrive와 동기화돼 있으면 설치 중에 오류가 날 수 있고, 경로가 너무 길면 Windows 경로 길이 제한에 걸려요.
2. **폴더 열기:** VS Code에서 **파일 → 폴더 열기**로 `rag_day5` 폴더를 열어요. 강의 폴더가 아니라 이 루트 폴더를 열어요.
3. **터미널에서 설치:** **터미널 → 새 터미널**(PowerShell)을 열고 아래를 실행해요.

```powershell
# uv와 Python 3.12가 준비됐는지 확인해요.
uv --version
uv python install 3.12
# 8개 강의에 필요한 패키지를 한 번에 설치해요. rag_day5 폴더에서 실행해요.
uv sync
```

`.venv` 폴더가 `rag_day5` 바로 아래에 하나 생기면 끝이에요. 4일차 패키지에 `networkx`(9장 3강)와 `pillow`(9장 4강)를 더했어요.

E5 모델(`intfloat/multilingual-e5-small`)은 전에 한 번 받았다면 그대로 다시 써요. 기본 실행에서 E5를 쓰는 강의는 8장 4강뿐이에요.

> **교안의 "실습 준비"와 다른 점:** 교안은 강의마다 `uv init`, `uv python pin`, `uv add`를 하라고 안내해요. 이 묶음에서는 위의 `uv sync` 한 번으로 대신하므로, **강의 폴더 안에서 `uv init`을 실행하지 마세요.** 실행하면 그 강의 폴더에만 환경이 따로 생겨요.

## 강의마다: 실행

8개 강의 모두 **`prepare.py` 없이 `main.py`부터** 실행해요. uv가 상위 폴더의 환경을 자동으로 찾아 써요.

```powershell
# 예: 8장 1강
cd ch08\rag_ch08_01
uv run main.py
uv run solution.py

# 다음 강의로 갈 때는 rag_day5에서 다시 이동해요.
cd ..\..\ch09\rag_ch09_01
uv run main.py
```

- 8장 3강 `main.py`는 `answer_review_08.json`, 8장 4강 `main.py`는 `comparison_08.json`을 만들어요. 9장 3강은 `graphrag_demo/input`, 9장 4강은 `visual_pages/*.png`를 만들어요.
- 기본 실행은 **생성 모델이나 API 키 없이** 동작해요. `RAGAS_NOT_RUN`, `GENERATION_NOT_RUN`, `GRAPHRAG_NOT_RUN`, `MODEL_NOT_RUN`은 정상 안내예요.
- 강의 폴더마다 교안 "기본 실습" 문제가 세 가지 파일로 들어 있어요. 통과하면 `✅ 정답이에요!`가 나와요.
  - `q_easy.py`: 교안의 빈칸(`____`) 그대로
  - `q_hard.py`: 같은 문제를 TODO로 바꾼 버전
  - `q_solution.py`: 교안 정답
- 퀴즈 파일은 `main.py`를 먼저 실행한 뒤 문제를 풀어요. 그래서 기본 예제 출력이 먼저 나와요.

## VS Code 편집기 설정 (import 밑줄이 보일 때)

Ctrl+Shift+P → **Python: Select Interpreter** → `rag_day5\.venv\Scripts\python.exe`를 골라요. 8개 강의 모두 이 하나로 돼요.

## 선택 실습

공용 환경을 바꾸지 않도록 **`uv add` 대신 `uv run --with …`** 로 필요한 패키지를 그 실행에만 붙여요. 처음 실행할 때 패키지를 내려받아 시간이 걸려요.

### 8장 3강: RAGAS (평가 LLM API 필요)

```powershell
cd ch08\rag_ch08_03
uv run main.py
uv run --with ragas==0.4.3 --with openai==2.54.0 --with langchain-community==0.3.31 run_ragas.py
uv run --with ragas==0.4.3 --with openai==2.54.0 --with langchain-community==0.3.31 run_ragas.py --show-recorded
```

- 첫 번째 `run_ragas.py`는 **API를 부르지 않는 준비 모드**예요. `"shape": [2, 384]`, `"generation_requests": 0`이면 정상이에요.
- 실제 평가(유료, 최대 20회 호출)는 `uv run configure_api.py`로 키를 `.env`에 저장한 뒤 아래를 실행해요. **`.env`는 제출하거나 공유하지 마세요.**

```powershell
uv run configure_api.py
uv run --env-file .env --with ragas==0.4.3 --with openai==2.54.0 --with langchain-community==0.3.31 run_ragas.py --model gpt-6-luna --execute
```

### 9장 1강 · 2강: Ollama

```powershell
ollama pull gemma3:4b-it-q4_K_M
$env:OLLAMA_MODEL = "gemma3:4b-it-q4_K_M"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
cd ch09\rag_ch09_01
uv run main.py --generate
uv run compare_contexts.py
cd ..\rag_ch09_02
uv run agent.py
```

### 9장 3강: Microsoft GraphRAG (LLM API 필요)

```powershell
cd ch09\rag_ch09_03
uv run main.py
uv run --with graphrag==3.2.0 check_setup.py
uv run show_recorded.py
```

- `check_setup.py`는 **API를 부르지 않는 준비 확인**이에요. `"document_shape": [10, 384]`, `"graphrag_index_executed": false`면 정상이에요.
- 실제 색인 · 질의(유료)는 교안 순서대로 `uv run configure_api.py` 다음에 `uv run --env-file .env --with graphrag==3.2.0 graph_local.py index --root graphrag_demo`처럼 실행해요.

### 9장 4강: ColPali (모델 다운로드 · 메모리 필요)

```powershell
cd ch09\rag_ch09_04
uv run main.py
uv run --with colpali-engine==0.3.18 --with accelerate visual_search.py
```

교안에서도 ColPali 모델 추론 결과는 검증하지 않았다고 밝혀요. 메모리가 부족하면 기본 실행 결과만 기록해요.

## 막힐 때

| 증상 | 확인할 것 |
| --- | --- |
| `uv sync` 중 `os error 396` (하드 링크 오류) | OneDrive 동기화 폴더예요. `setx UV_LINK_MODE copy`를 실행하고 터미널을 새로 연 뒤 다시 `uv sync` 해요. 압축을 동기화되지 않는 폴더에 다시 푸는 것도 방법이에요 |
| `.venv\Lib\site-packages\…py` 파일이 없다는 `FileNotFoundError` | 압축을 푼 경로가 너무 길어요(Windows 경로 260자 제한). `C:\rag`처럼 짧은 경로에 다시 풀고 `uv sync` 해요 |
| `answer_review_08.json` · `comparison_08.json`이 없음 | 그 강의 폴더에서 `uv run main.py`를 먼저 실행해요 |
| `RAGAS_NOT_RUN` · `GENERATION_NOT_RUN` 등 | 기본 실행의 정상 안내예요. 모델 점수를 계산하지 않았다는 뜻이에요 |
| 9장 4강 PNG에 한글이 깨짐 | `C:\Windows\Fonts\malgun.ttf`(맑은 고딕)가 있는지 확인해요 |
| `--generate` · `agent.py`에서 Connection refused | Ollama 앱이 실행 중인지, `OLLAMA_BASE_URL`이 `http://localhost:11434`인지 확인해요 |
| `KeyError: 'OLLAMA_MODEL'` · model not found | `ollama list`에 나온 태그를 `OLLAMA_MODEL`에 정확히 넣어요 |
| API 인증 · 모델 권한 오류 | `.env`의 키와 `--env-file .env` 사용 여부를 확인해요. 미완료를 0점으로 기록하지 않아요 |
| HF 토큰 · symlink · `position_ids UNEXPECTED` 경고 | 모델을 받거나 불러올 때 나오는 안내 문구예요. 실행 결과에는 영향이 없어요 |
| `ModuleNotFoundError` | `rag_day5` 폴더에서 `uv sync`를 했는지, `uv run`으로 실행했는지 확인해요. 선택 실습 패키지는 `--with`를 붙였는지 확인해요 |
| 강의 폴더에 `pyproject.toml`이 생겼어요 | 실수로 `uv init`을 실행한 거예요. 그 강의 폴더의 `pyproject.toml`, `.python-version`, `.venv`를 지우면 다시 공용 환경을 써요 |

## 검증 기록

- 2026-10-25 · Windows 11 · Python 3.12에서 확인했어요.
- 8개 강의의 `main.py` · `solution.py`를 공용 환경으로 실행한 결과가 교안의 "전체 기본 실행 결과"와 같았어요 (예: 8-1 dev 12 · test 8 · 교집합 [], 8-2 k=3 Hit 0.9 · Recall 0.9, 8-3 수동 비율 A 1.0 · B 0.5 · C 1.0, 8-4 dev wins ['q10'], 9-1 child 80 · parent 148 · 예산 70 → 54자, 9-2 candidates_ready · repeated_query · search_limit, 9-3 노드 10 · 간선 8, 9-4 MaxSim A 2.0 · B 1.4142).
- API 없는 선택 실습 준비 모드도 확인했어요: 8-3 `run_ragas.py` shape [2, 384] · 요청 0회, 9-3 `check_setup.py` 문서 [10, 384] · 색인 미실행.
- 퀴즈 8개 모두 `q_solution.py`가 통과하고, `q_easy.py` 빈칸을 정답으로 채우면 통과하는 것을 확인했어요.
