from flask import Blueprint, request, current_app as app
from project_app.modules import downloader, db, pandas_tool, ml_tool, pickle_tool
from dotenv import load_dotenv
import os

load_dotenv()

REFRESH_PASSWORD = os.environ.get('REFRESH_PASSWORD')

adminBp = Blueprint('admin', __name__, url_prefix='/admin')

@adminBp.route('/refresh', methods=['POST'])
def refresh():
    body = request.get_json()
    # 패스워드 검사
    if (body is None) or ('password' not in body):
        return {"message" : "패스워드가 없습니다."}, 400
    password = body['password']
    if password != REFRESH_PASSWORD:
        return {"message" : "잘못된 패스워드입니다."}, 400
    # 로컬에서 캐글 토큰 확인후 캐글에 있는 데이터셋을 다운로드
    downloader.save_csv()
    
    # postgre DB에 테이블을 재생성
    db.recreate_table()
    
    # 데이터 셋 csv를 pandas 데이터프레임으로 저장함
    df = pandas_tool.read_csv_dataset()
    
    # 'dataset'테이블에 import
    pandas_tool.import_db(df, 'dataset')
    
    # 데이터셋을 랭글링합니다.
    df_fillna = pandas_tool.get_wrangled_df(df)

    df_nonTest, df_test = ml_tool.get_splitted_df(df_fillna)
    app.models = ml_tool.create_models(df_nonTest)
    pickle_tool.save_models(app.models)
    print('model is created')
    app.score = ml_tool.create_roc_auc_score(df_test, app.models)
    pickle_tool.save_score(app.score)
    print('score is calculated')

    return {'message' : '모델 재생성이 완료되었습니다. 서버를 다시 시작해주세요.'}, 200

@adminBp.route('/test', methods=['GET'])
def test():
    return REFRESH_PASSWORD