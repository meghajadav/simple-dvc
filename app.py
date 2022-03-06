import os
import yaml
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np 

params_path = 'params.yaml'

app = Flask(__name__)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file) 
    return config

def predict(data):
    config = read_params(params_path)
    saved_model_path = config['web_app_dir']
    model = joblib.load(saved_model_path)
    pred = model.predict(data)
    print(pred)
    return pred[0]

def api_response(data):
    try:
        data = np.array([list(request.json.values())])
        response = predict(data)
        response = {"response":response}
        return response
    except Exception as e:
        print(e)
        error = {'error': 'something went wrong. Please try again.'}
        return error

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method=='POST':
        try:
            if request.json:
                response = api_response(request)
                return jsonify(response)

        except Exception as e:
            print(e)
            error = {'error':'Something went wrong. Please try again.'}
            return error
    
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
