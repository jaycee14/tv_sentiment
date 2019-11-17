from flask import Flask
from api import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api/v1')

if __name__ == '__main__':
	print("running api server")
	app.run(debug=True, host='0.0.0.0', port=8008)