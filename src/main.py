from flask import Flask
from db_init import ApplicationBase, DB_URL
import logging
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
base = ApplicationBase()
db = base.Session()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('secret-logger')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
