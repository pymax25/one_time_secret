import logging
import sys

from flask import abort, Flask, jsonify, request

from exceptions import SecretNotFound
from daos import SecretDAO
from db_init import DB_URL, ApplicationBase
from services import CreateSecretService, GetSecretService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
base = ApplicationBase()
db = base.Session()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('secret-logger')


@app.route("/secret", methods=["POST"])
def create_secret():
    secret = request.json.get("secret")
    secret_dao = SecretDAO(db=db)
    create_secret_service = CreateSecretService(
        secret_dao=secret_dao
    )
    secret_id = create_secret_service.execute(secret=secret)
    return {"secret_id": secret_id}


@app.route("/secret/<secret_id>", methods=["POST"])
def get_secret(secret_id):
    secret_dao = SecretDAO(db=db)
    get_secret_service = GetSecretService(
        secret_dao=secret_dao
    )
    try:
        encoded_secret = get_secret_service.execute(secret_id=secret_id)
        return jsonify({"your_secret": encoded_secret})
    except SecretNotFound:
        abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
