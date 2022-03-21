## train the model
## save the model 
## evaluate the model

import os
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from get_data import read_params
import joblib
import json
import numpy as np
import argparse
import mlflow
from urllib.parse import urlparse

def eval_model(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def train_and_evaluate_model(config_path):
    config = read_params(config_path)

    train_data_path = config['split_data']['train_data']
    test_data_path = config['split_data']['test_data']
    
    train = pd.read_csv(train_data_path, sep=',')
    test = pd.read_csv(test_data_path, sep=',')

    l1_ratio = config['estimators']['ElasticNet']['params']['l1_ratio']
    alpha = config['estimators']['ElasticNet']['params']['alpha']

    target = config['base']['target_col']

    train_x = train.drop([target], axis=1)
    test_x = test.drop([target], axis=1)

    train_y = train[target]
    test_y = test[target]

    random_state = config['base']['random_state']

    save_model_dir = config['models_dir']
#-----------------------------------MLFLOW------------------------------------
    mlflow_config = config['mlflow_config']
    remote_server_uri = mlflow_config['remote_server_uri']
    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment(mlflow_config['experiment_name'])
    
    with mlflow.start_run(run_name = mlflow_config['run_name']) as mlops_run:
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)
        lr.fit(train_x, train_y)

        preds = lr.predict(test_x)

        rmse, mae, r2 = eval_model(test_y, preds)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric('rmse', rmse)
        mlflow.log_metric('mae', mae)
        mlflow.log_metric('r2', r2)

        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme

        if tracking_url_type_store != 'file':
            mlflow.sklearn.log_model(lr,
            "model", 
            registered_model_name = mlflow_config['registered_model_name'])
        else:
            mlflow.sklearn.load_model(lr, "model")

    # print('rmse:: ', rmse)
    # print('mae:: ', mae)
    # print('r2:: ', r2)

    # scores_file = config['reports']['scores']
    # params_file = config['reports']['params']

    # with open(scores_file, 'w') as f:
    #     scores = {
    #         'rmse':rmse,
    #         'mae': mae,
    #         'r2': r2
    #     }
    #     json.dump(scores, f, indent=4)

    # with open(params_file, 'w') as f:
    #     params = {
    #         'alpha':alpha,
    #         'l1_ratio': l1_ratio,
    #     }
    #     json.dump(params, f, indent=4)

    # os.makedirs(save_model_dir, exist_ok=True)
    # model_path = os.path.join(save_model_dir, 'model.joblib')
    # # lr.save('model_elastic.sav', save_model_dir)
    # joblib.dump(lr, model_path)

if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parse_arg = args.parse_args()
    train_and_evaluate_model(config_path=parse_arg.config)
