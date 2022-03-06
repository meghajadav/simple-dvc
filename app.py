import os
import yaml
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np 

params_path = 'params.yaml'
webapp_path = 'webapp'
static_dir = os.path.join(webapp_path, 'static')
template_dir = os.path.join(webapp_path, 'templates')

app = Flask(__name__, static_folder =static_dir, template_folder=template_dir)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file) 
    return config

def predict(data):
    config = read_params(params_path)
    model_path = config['web_app_dir']
    model = joblib.load(model_path)
    pred = model.predict(data)
    print(pred)
    return pred[0]

def api_response(data):
    try:
        # print('---------------', request.json.values())
        data = np.array([list(request.json.values())])
        response = predict(data)
        response = {"response":response}
        return response
    except Exception as e:
        print(e)
        error = {'error': str(e)}
        return error

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method=='POST':
        try:
            if request.form:
                data = dict(request.form).values()
                data = [list(map(float, data))]
                response = predict(data)
                return render_template('index.html', response=response)
       
            elif request.json:
                response = api_response(request)
                # print('--------------------------',request)
                return jsonify(response)

        except Exception as e:
            print(e)
            error = {'error':str(e)}
            return render_template('404.html', error=error)
    else:
        return render_template('index.html')
    
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
