
from fastai.text import load_learner, defaults
import torch

from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

defaults.device = torch.device('cpu')

model = load_learner(path='.', file='export_32.pkl')


@api.route('/test')
def test():
    return jsonify('api test')


@api.route('/predict', methods=['POST'])
def predict():
    input = request.json
    text = input['text']

    cat, ten, score = model.predict(text)
    return jsonify({'label': cat.__str__(), 'score': score[ten].item(), 'model': 'fastai'})

