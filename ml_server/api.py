# standard imports
import json
import os
import uuid
import io
import time
import random

# third party imports
import pandas as pd
from fastai.text import *

from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

defaults.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = load_learner('.')


@api.route('/test')
def test():
    return jsonify('api test')


@api.route('/predict', methods=['POST'])
def predict():
    input = request.json
    text = input['text']

    # this is the real deal
    cat, ten, score = model.predict(text)
    return jsonify({'label': cat.__str__(), 'score': score[ten].item()})

    # this is a test reply until docker compose catches up with cuda
    #return jsonify(('Test', 42))
