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

ml_addr = "ml_server:8008"  # method to use once in the same compose group
# ml_addr = "192.168.1.123:8008"

app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_user, pw=db_password, url=host_addr, db=db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

twitter = Twitter_Retrieve()
NUMBER_OF_TWEETS = 100

@app.route('/')
def show_all():
    return render_template('show_all.html', shows=Shows.query.all())


@app.route('/show_comments')
def show_comments():
    comments = db.session.query(Comments).order_by(Comments.query_id.desc())
    return render_template('show_comments.html', comments=comments)


@app.route('/add')
def add():
    show_name = 'parks and recreation'
    service = ''
    show = Shows(show_name, service, True)

    db.session.add(show)
    db.session.commit()

    query = Queries(show.id, -1, f'{show_name} {service}')
    db.session.add(query)
    db.session.commit()

    return render_template('show_all.html', shows=Shows.query.all())


@app.route('/toggle/<id_val>')
def toggle_active(id_val):
    show = Shows.query.filter_by(id=id_val).one()
    show.active = not show.active
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

    # get active shows
    shows = Shows.query.filter_by(active=True).all()
    show_list = [show.id for show in shows]

    # get last ids for active shows, need latest
    queries = db.session.query(Queries.show_id, Queries.query_string,
                               func.max(Queries.last_extract_id).label('last_extract_id')) \
        .filter(Queries.show_id.in_(show_list)) \
        .group_by(Queries.show_id, Queries.query_string)

    for query in queries:
        # query twitter using the latest since_id
        results, last_id = twitter.search(query.query_string, since_id=query.last_extract_id, num_entries=NUMBER_OF_TWEETS)

        if len(results) > 0:

            # record this new twitter query
            new_query = Queries(query.show_id, last_id, query.query_string)
            db.session.add(new_query)
            db.session.commit()
            new_query_id = new_query.id

            # run results through model
            for res in results:
                twitter_text = res['text'][:299]
                twitter_date = res['date']
                response = requests.post(url, json={"text": twitter_text}).json()
                comments.append(
                    Comments(query.show_id, twitter_text, response['label'], response['score'], response['model'],
                             new_query_id,
                             twitter_date))
            #
            db.session.add_all(comments)
            db.session.commit()

    # store results and messages
    return redirect(url_for('show_comments'))


if __name__ == '__main__':
    print("running tv sentiment app")

    db.app = app
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=80)

