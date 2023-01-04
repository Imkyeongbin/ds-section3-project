import pandas as pd
from project_app.modules import db

def read_csv_dataset():
    return pd.read_csv('data/healthcare-dataset-stroke-data.csv', index_col='id')

def import_db(df, string):
    df.to_sql(string, db.get_engine(), if_exists='replace')
    
def export_db(string):
    return pd.read_sql_table(string, db.get_engine(), index_col='id')

def get_wrangled_df(df):
    df_fillna = df
    df_fillna['bmi'].fillna(round(df['bmi'].mean(), 1), inplace=True)
    # print(df_fillna.columns)
    # object로 들어온 값을 전부 category로 변경 => xgboost 사용시 enable_categorical 옵션으로 인코딩 없이 사용가능
    for col in ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']:
        df_fillna[col] = df_fillna[col].astype('category')
    return df_fillna

def get_single_df(dict_obj):
    return get_wrangled_df(pd.DataFrame.from_dict([dict_obj]))