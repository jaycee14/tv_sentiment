

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
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd


def main():

	print("running my app")

	db_name = os.environ['POSTGRES_DB']
	db_user = os.environ['POSTGRES_USER']
	db_password = os.environ['POSTGRES_PASSWORD']
	host_addr = "database:5432"
	engine_params = (f'postgresql+psycopg2://{db_user}:{db_password}@{host_addr}/{db_name}')
	num_tries = 1
	max_num_tries = 10

	while True:
		try:
			engine = create_engine(engine_params)
			conn = engine.raw_connection()
			cur = conn.cursor()
			break
		except (sqlalchemy.exc.OperationalError, psycopg2.OperationalError):
            # Use binary exponential backoff
            #- i.e. sample a wait between [0..2^n]
            #when n = number of tries.
			time.sleep(random.randint(0, 2**num_tries))
			if num_tries > max_num_tries:
				raise IOError("Database unavailable")
				num_tries += 1


	# a dictionary of tables and schemas.
	schemas = {
			"shows":"(show_id SERIAL PRIMARY KEY, name VARCHAR(128))",
			"comments":"(comment_id SERIAL PRIMARY KEY, show_id INTEGER NOT NULL, comment VARCHAR(280), score FLOAT)",
	} #dictionary for us to store our schemas

	for table, schema in schemas.items():
		cur.execute(
			sql.SQL("CREATE TABLE IF NOT EXISTS {} {}").format(
			sql.Identifier(table), sql.SQL(schema))
		)

	conn.commit()

	val1 = 'daybreak'

	#cur.execute("INSERT INTO shows (name) VALUES (%s)", (val1,))
	#conn.commit()

	cur.execute("SELECT * FROM shows")
	res = cur.fetchall()
	for r in res:
		print(r)

	print('finishing my app')
	cur.close()


if __name__ == '__main__':
	main()
