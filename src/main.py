import logging
import sys
import time

from flask import Flask, abort, jsonify, request

from config import config
from daos import SecretDAO
from db_init import DB_URL, ApplicationBase
from exceptions import SecretNotFound
from services import CreateSecretService, GetSecretService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
base = ApplicationBase()
db = base.Session()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('secret-logger')
request_count = {}
limit = config.REQUESTS_PER_MINUTE_LIMIT


@app.before_request
def limit_requests():
    user = request.remote_addr
    current_time = int(time.time())
    if user not in request_count:
        request_count[user] = [(current_time, 1)]
    else:
        request_count[user].append((current_time, 1))
        while request_count[user] and request_count[user][0][0] < current_time - 60:
            request_count[user].pop(0)
    total_requests = sum([count for _, count in request_count[user]])
    if total_requests > limit:
        logger.info(request_count)
        return f"Amount of requests exceeded {limit} in 1 minute", 429


@app.route("/secret", methods=["POST"])
def create_secret():
    secret = request.json.get("secret")
    if not secret:
        return jsonify({'error': 'Invalid data: "secret" is missing'}), 400
    secret_dao = SecretDAO(db=db)
    create_secret_service = CreateSecretService(
        secret_dao=secret_dao
    )
    try:
        secret_id = create_secret_service.execute(secret=secret)
        return {"secret_id": secret_id}
    except Exception as e:
        logger.error(e)
        return jsonify({'error': 'Internal server error'}), 502


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
