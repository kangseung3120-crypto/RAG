"""Register local E5 before invoking the actual GraphRAG CLI."""
from local_e5_provider import register
from graphrag.cli.main import app

# GraphRAG CLI가 설정을 읽기 전에 local_e5 공급자를 등록해요.
# 그 뒤 명령 인수를 실제 GraphRAG CLI에 넘기므로 index/query 동작은 공식 구현이 수행해요.
register()
app(prog_name='graph_local')
