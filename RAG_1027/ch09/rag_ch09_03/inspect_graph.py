"""Read actual GraphRAG outputs without calling generation or embedding APIs."""
import json
from pathlib import Path
import pandas as pd

# 실제로 색인한 프로젝트의 Parquet 산출물을 읽어요.
# 필수 파일이 없으면 과거 검수 기록으로 대신 채우지 않고 먼저 색인을 완료하라고 안내해요.
folder=Path(__file__).resolve().parent/'graphrag_demo/output'
names=['documents','text_units','entities','relationships','communities','community_reports']
if not all((folder/f'{name}.parquet').exists() for name in names):
    raise SystemExit('색인 산출물이 아직 없어요. 실제 색인을 완료한 뒤 실행하세요.')
tables={name:pd.read_parquet(folder/f'{name}.parquet') for name in names}
coverage=[]
# 각 원문의 text_unit_ids와 엔티티/관계/커뮤니티의 근거 ID가 연결되는지 세어요.
# 어떤 원문이 그래프 생성 과정에서 빠졌는지 찾기 위한 구조 검수예요.
for _,document in tables['documents'].iterrows():
    units=set(document['text_unit_ids'])
    coverage.append({'document':document['title'],**{
        name:sum(bool(units.intersection(ids)) for ids in tables[name]['text_unit_ids'])
        for name in ['entities','relationships','communities']}})
# 모든 문서가 연결됐어도 관계 방향, 승인 시점, 예외 조건이 정확하다는 뜻은 아니에요.
# 개수 확인 뒤 중요한 질의를 실행하고 원문과 답변을 대조해야 해요.
report={'counts':{name:len(table) for name,table in tables.items()},'coverage':coverage,
        'all_documents_represented':all(all(row[name]>0 for name in
            ['entities','relationships','communities']) for row in coverage)}
Path('graph_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
print('문서별 연결 확인과 답변의 의미 검수는 별도예요. 승인 시점과 예외는 원문에 대조하세요.')
