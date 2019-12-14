# standard imports
import os

import requests
from flask import Flask, render_template, jsonify, redirect, url_for
from sqlalchemy import func

from db_models import db, Shows, Comments, Queries
from twitter_model import Twitter_Retrieve

db_name = os.environ['POSTGRES_DB']
db_user = os.environ['POSTGRES_USER']
db_password = os.environ['POSTGRES_PASSWORD']
host_addr = os.environ['DB_HOST']

# ml_addr = "ml_server:8008"
ml_addr = "192.168.1.104:8008"

app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_user, pw=db_password, url=host_addr, db=db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

twitter = Twitter_Retrieve()


@app.route('/')
def show_all():
    return render_template('show_all.html', shows=Shows.query.all())


@app.route('/show_comments')
def show_comments():
    return render_template('show_comments.html', comments=Comments.query.all())


@app.route('/add')
def add():
    show = Shows('v wars', 'netflix', True)

    db.session.add(show)
    db.session.commit()

    query = Queries(show.id, -1, 'v wars netflix')
    db.session.add(query)
    db.session.commit()

    return render_template('show_all.html', shows=Shows.query.all())


@app.route('/predict_test')
def predict_test():
    url = f'http://{ml_addr}/api/v1/predict'
    response = requests.post(url, json={"text": "daybreak is amazing"})
    return jsonify(response.json())


@app.route('/run')
def run_model():
    url = f'http://{ml_addr}/api/v1/predict'
    comments = []

    # get shows
    shows = Shows.query.filter_by(active=True).all()

    show_list = [show.id for show in shows]

    # get last ids for shows, need latest
    queries = db.session.query(Queries.show_id, Queries.last_extract_id, Queries.query_string,
                               func.max(Queries.query_date).label('query_date')) \
        .group_by(Queries.show_id, Queries.last_extract_id, Queries.query_string)

    temp_put = []

    for query in queries:
        temp_put.append([query.show_id, query.last_extract_id, query.query_string, query.query_date])

        # query twitter using the latest since_id
        results, last_id = twitter.search(query.query_string, since_id=query.last_extract_id)

        # record this new twitter query
        new_query = Queries(query.show_id, last_id, query.query_string)
        db.session.add(new_query)
        db.session.commit()
        new_query_id = new_query.id

        # run results through model
        for res in results:
            twitter_text = res['text']
            twitter_date = res['date']
            response = requests.post(url, json={"text": twitter_text}).json()
            comments.append(
                Comments(query.show_id, twitter_text, response['label'], response['score'], response['model'], new_query_id,
                         twitter_date))
    #
    db.session.add_all(comments)
    db.session.commit()

    # store results and messages
    return redirect(url_for('show_comments'))



print("running my app")

db.app = app
db.init_app(app)
db.create_all()

app.run(debug=True, host='0.0.0.0', port=80)

