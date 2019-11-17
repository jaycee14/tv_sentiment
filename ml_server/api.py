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

defaults.device = torch.device('cuda')

model = load_learner('.')


@api.route('/test')
def test():
    return jsonify('api test')


@api.route('/predict', methods=['POST'])
def predict():
    input = request.json
    text = input['text']

    cat, ten, score = model.predict(text)

    return jsonify((cat.__str__(), score[ten].item()))