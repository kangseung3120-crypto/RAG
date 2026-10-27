"""Store a lesson-specific key using hidden input. Does not call an API."""
import getpass
from pathlib import Path

# 키는 이 강의 폴더의 .env에만 저장하고 기존 파일이 있으면 덮어쓰지 않아요.
# .env는 개인 설정이므로 수강생 자료 ZIP에 포함하거나 공유하지 마세요.
target = Path(__file__).resolve().parent/'.env'
if target.exists():
    raise SystemExit('이 강의 폴더에 .env가 이미 있어요. 기존 설정을 확인하세요.')
# getpass는 터미널에 키가 보이지 않게 입력받아요.
# 따옴표나 공백이 포함된 입력은 환경변수 한 줄로 안전하게 저장하기 어려워 거부해요.
key = getpass.getpass('API 키를 입력하고 Enter를 누르세요. 입력값은 표시되지 않아요: ').strip()
if not key or any(c.isspace() for c in key) or any(c in key for c in ['"',"'"]):
    raise SystemExit('키를 저장하지 않았어요. 공백이나 따옴표 없이 입력하세요.')
# x 모드는 파일이 이미 있으면 실패하는 생성 전용 모드예요.
# 이 파일은 저장만 하며 실행할 때 uv run --env-file .env로 읽어야 설정이 전달돼요.
with target.open('x',encoding='utf-8',newline='\n') as stream:
    stream.write('OPENAI_API_KEY='+key+'\n')
print('현재 강의 폴더의 .env에 저장했어요. API 요청은 하지 않았어요.')
