import pytest
from prediction_service.prediction import form_response, api_response
import prediction_service

input_data = {
    'incorrect_range':
    {
    "fixed_acidity":789789,
    "volatile_acidity": 555,
    "citric_acid": 99,
    "residual_sugar": 99,
    "chlorides": 12,
    "free_sulfur_dioxide": 789,
    "total_sulfur_dioxide": 75,
    "density": 2,
    "pH": 33,
    "sulphates": 9,
    "alcohol": 9
    },

    'incorrect_col':
    {        
    "fixed acidity":789789,
    "volatile acidity": 555,
    "citric acid": 99,
    "residual sugar": 99,
    "chlorides": 12,
    "free sulfur dioxide": 789,
    "total sulfur dioxide": 75,
    "density": 2,
    "pH": 33,
    "sulphates": 9,
    "alcohol": 9

    },

    'correct_range':
    {
    "fixed_acidity":5,
    "volatile_acidity": 0.5,
    "citric_acid": 0.5,
    "residual_sugar": 10,
    "chlorides": 0.5,
    "free_sulfur_dioxide": 22,
    "total_sulfur_dioxide": 75,
    "density": 1,
    "pH": 3,
    "sulphates": 1,
    "alcohol": 9
    }
}

Target_range={
    'min':3.0,
    'max':8.0
}

def test_form_response_correct_range(data = input_data['correct_range']):
    res = form_response(data) 
    assert Target_range['min'] <= res['response'] <= Target_range['max']

def test_api_response_correct_range(data = input_data['correct_range']):
    res = api_response(data)
    assert Target_range['min'] <= res['response'] <= Target_range['max']

def test_form_response_incorrect_range(data = input_data['incorrect_range']):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)

def test_api_response_incorrect_range(data = input_data['incorrect_range']):
    res = api_response(data)
    assert res['response'] == prediction_service.prediction.NotInRange().message

def test_api_response_incorrect_col(data = input_data['incorrect_col']):
    res = api_response(data)
    assert res['response'] == prediction_service.prediction.NotInCols().message
