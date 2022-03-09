import os
import joblib
import yaml
import json
import numpy as np


schema_file = os.path.join('prediction_service','schema_in.json')
params_path = 'params.yaml'

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir = config['web_app_dir']
    model = joblib.load(model_dir)
    predic = model.predict(data).tolist()[0]
    
    try:
        if 3 <= predic <= 8:
            return predic
        else:
            raise NotInRange
    
    except NotInRange:
        return 'Unexpected Range.'
        

class NotInRange(Exception):
    def __init__(self, message='Values not in range.'):
        self.message = message
        super().__init__(self.message)

class NotInCols(Exception):
    def __init__(self, message="Not in columns."):
        self.message = message
        super().__init__(self.message)

def getSchema(schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema 


def validate_input(dict_response):
    def validate_cols(col):
        schema = getSchema(schema_file)
        cols = schema.keys()
        if col not in cols:
            raise NotInCols

    def validate_vals(col, val):
        schema = getSchema(schema_file)
        if not (schema[col]['min'] <= float(val) <= schema[col]['max'] ):
            raise NotInRange
        

    for col, val in dict_response.items():
        print(validate_cols(col))
        print(validate_vals(col, val))
    return True

def form_response(dict_response):
    if validate_input(dict_response):
        data = dict_response.values()
        data = [list(map(float, data))]
        prediction = predict(data)
        response = {'response':prediction}
        return response 

def api_response(dict_response):
    try:
        if validate_input(dict_response):
            data = np.array([list(dict_response.values())])
            predic = predict(data)
            response = {'response':predic}
            return response
    except Exception as e:
            response = {'Expected range':getSchema(schema_file) , "response": str(e)}
            return response 