import kaggle
import os

DATA_PATH = os.path.join(os.getcwd() + '/data')

def save_csv():
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('fedesoriano/stroke-prediction-dataset', path=DATA_PATH, unzip=True)