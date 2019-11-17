

#standard imports
import json
import os
import uuid
import io
import time
import random

#third party imports
import psycopg2
from psycopg2 import sql
# import sqlalchemy
# from sqlalchemy import create_engine
import pandas as pd

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db_name = os.environ['POSTGRES_DB']
db_user = os.environ['POSTGRES_USER']
db_password = os.environ['POSTGRES_PASSWORD']
host_addr = "database:5432"


app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_user,pw=db_password,url=host_addr,db=db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

db = SQLAlchemy(app)

class Shows(db.Model):
	"""docstring for Shows"""

	id = db.Column('show_id',db.Integer, primary_key=True)
	name = db.Column('name', db.String(100))
	service = db.Column('service', db.String(20))

	def __init__(self, name, service):
		self.name = name
		self.service = service

		
@app.route('/')
def show_all():
   return render_template('show_all.html', shows = Shows.query.all() )

if __name__ == '__main__':
	print("running my app")
	db.create_all()
	app.run(debug=True, host='0.0.0.0', port=80)


