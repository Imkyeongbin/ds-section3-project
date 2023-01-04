from flask import Blueprint, request, render_template, current_app as app
from project_app.modules import pandas_tool, ml_tool
from dotenv import load_dotenv
import os

load_dotenv()

REFRESH_PASSWORD = os.environ.get('REFRESH_PASSWORD')

resultBp = Blueprint('result', __name__, url_prefix='/result')

@resultBp.route('/', methods=['POST'])
def result():
    # 폼데이터로 받은 데이터를 각 이름 변수에 저장
    gender = request.form.get('gender')
    age = int(request.form.get('age'))
    hypertension = int(request.form.get('hypertension'))
    heart_disease = int(request.form.get('heart_disease'))
    ever_married = request.form.get('ever_married')
    work_type = request.form.get('work_type')
    Residence_type = request.form.get('Residence_type')
    avg_glucose_level = float(request.form.get('avg_glucose_level'))
    bmi = float(request.form.get('bmi'))
    smoking_status = request.form.get('smoking_status')
    # 각 변수를 dict로 변경
    dict_obj = {
        "gender": gender,
        "age" : age,
        "hypertension" : hypertension,
        "heart_disease" : heart_disease,
        "ever_married" : ever_married,
        "work_type" : work_type,
        "Residence_type" : Residence_type,
        "avg_glucose_level" : avg_glucose_level,
        "bmi" : bmi,
        "smoking_status" : smoking_status
    }

    single_df = pandas_tool.get_single_df(dict_obj)
    stroke_proba = ml_tool.get_predict_proba(single_df, app.models)

    return render_template('result.html', stroke=stroke_proba), 200
