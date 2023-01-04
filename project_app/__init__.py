# __init__.py

from flask import Flask
from project_app.modules import downloader, db, pandas_tool, ml_tool, pickle_tool

def create_app():
  app = Flask(__name__, static_url_path='')

  from project_app.views.index import indexBp
  from project_app.views.admin import adminBp
  from project_app.views.result import resultBp
  app.register_blueprint(indexBp)
  app.register_blueprint(adminBp)
  app.register_blueprint(resultBp)

  downloader.save_csv()
  
  df = init_df()
  df_nonTest, df_test = ml_tool.get_splitted_df(df)
  app.models = init_models(df_nonTest)
  app.score = init_score(df_test, app.models)
  return app

def init_df():
  df = None
  table_name = 'dataset'
  try:
    df = pandas_tool.export_db(table_name)
  except:
    db.recreate_table()
    df = pandas_tool.read_csv_dataset()
    pandas_tool.import_db(df, table_name)

  df_fillna = pandas_tool.get_wrangled_df(df)

  print('init_df is done')  
  return df_fillna

def init_models(df_nonTest):
  models = None
  try:
    models = pickle_tool.load_models()
    print('model is loaded')
  except:
    models = ml_tool.create_models(df_nonTest)
    pickle_tool.save_models(models)
    print('model is created')
  print('init_models is done')
  return models

def init_score(df_test, models):
  score = None
  try:
    score = pickle_tool.load_score()
    print('score is loaded')
  except:
    score = ml_tool.create_roc_auc_score(df_test, models)
    pickle_tool.save_score(score)
    print('score is calculated')
  print('init_score is done')
  return score


if __name__ == "__main__":
  app = create_app()
  app.run()