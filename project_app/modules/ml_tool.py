from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.utils import class_weight
import xgboost as xgb
import numpy as np
import gc
import pandas as pd

gc.enable()

target = 'stroke'
KFOLD = 10

def get_splitted_df(df):
    df_nonTest, df_test = train_test_split(df, test_size= 0.2, random_state=42, stratify=df[target])
    return df_nonTest, df_test

def get_X_y(df):
    X_df = df.drop(columns=target)
    y_df = df[target]
    return X_df, y_df

def get_classifier():
    return xgb.XGBClassifier(   max_depth=5,
                                colsample_bytree=0.7,
                                n_estimators=2000,
                                learning_rate=0.2,
                                objective='binary:logistic', 
                                verbosity =1,
                                eval_metric  = 'auc',
                                tree_method='gpu_hist',
                                n_jobs=3,
                                enable_categorical=True,
                                early_stopping_rounds= 100  )

def create_models(df_nonTest):
    X_nonTest, y_nonTest = get_X_y(df_nonTest)

    folds = StratifiedKFold(n_splits=KFOLD)
    model_xgb = get_classifier()

    models = []
    for fold_index, (train_index, val_index) in enumerate(folds.split(X_nonTest,y_nonTest)):
        print('Batch {} started...'.format(fold_index))
        gc.collect()

        classes_weights = class_weight.compute_sample_weight(
            class_weight='balanced',
            y=y_nonTest.iloc[train_index]
        )

        bst = model_xgb.fit(X_nonTest.iloc[train_index],y_nonTest.iloc[train_index],
                eval_set = [(X_nonTest.iloc[val_index],y_nonTest.iloc[val_index])],
                verbose= 200,
                sample_weight= classes_weights
                )
        models.append(model_xgb)

    return models

def create_roc_auc_score(df_test, models):
    X_test, _ = get_X_y(df_test)

    pred = np.zeros(df_test.shape[0])
    for model in models:
        pred += model.predict_proba(X_test)[:,1] / KFOLD
    df_pred = pd.DataFrame(pred, columns = [target])
    return roc_auc_score(df_pred > 0.5, df_test[target])

def get_predict_proba(X_test1, models):
    pred = 0
    for model in models:
        pred += model.predict_proba(X_test1)[:,1] / KFOLD
    return pred