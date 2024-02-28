import logging
import sys
import time
import traceback

from flask import Flask, jsonify, request

from config import config
from daos import SecretDAO
from db_init import DB_URL, ApplicationBase
from exceptions import SecretNotFound
from services import CreateSecretService, GetSecretService
from utils import is_valid_uuid

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("secret-logger")

request_count = {}
limit = config.REQUESTS_PER_MINUTE_LIMIT


@app.before_request
def limit_requests():
    user = request.remote_addr
    logger.info(f"Received POST request from user {user}.")
    current_time = int(time.time())
    if user not in request_count:
        request_count[user] = [(current_time, 1)]
    else:
        request_count[user].append((current_time, 1))
        while request_count[user] and request_count[user][0][0] < current_time - 60:
            request_count[user].pop(0)
    total_requests = sum([count for _, count in request_count[user]])
    if total_requests > limit:
        logger.info(f"User {user} exceeded request limit per 1 minute. Current amount is {total_requests}")
        return jsonify({"error": f"Amount of requests exceeded {limit} per 1 minute"}), 429


@app.route("/secret", methods=["POST"])
def create_secret():
    if request.content_type != "application/json":
        logger.error("Content type must be application/json.")
        return jsonify({"error": "Content type must be application/json."}), 406
    secret = request.json.get("secret")
    if not secret:
        logger.error("Invalid data: 'secret' is missing.")
        return jsonify({"error": "Invalid data: 'secret' is missing"}), 400
    if not isinstance(secret, str):
        logger.error("Invalid data: 'secret' must be a string.")
        return jsonify({"error": "Invalid data: 'secret' must be a string"}), 400
    logger.info(f"Got a new secret request with data {secret}")
    base = ApplicationBase()
    db = base.Session()
    secret_dao = SecretDAO(db=db)
    create_secret_service = CreateSecretService(
        secret_dao=secret_dao,
        logger=logger,
    )
    try:
        secret_id = create_secret_service.execute(secret=secret)
        return {"secret_id": secret_id}
    except Exception as e:
        logger.error(f"error: {e}")
        return jsonify({"error": "Internal server error"}), 502


@app.route("/secret/<secret_id>", methods=["POST"])
def get_secret(secret_id):
    if not is_valid_uuid(secret_id):
        logger.error("Invalid UUID format in secret_id")
        return jsonify({"error": "Invalid UUID format in secret_id"}), 400
    base = ApplicationBase()
    db = base.Session()
    secret_dao = SecretDAO(db=db)
    get_secret_service = GetSecretService(
        secret_dao=secret_dao,
        logger=logger,
    )
    try:
        encoded_secret = get_secret_service.execute(secret_id=secret_id)
        logger.info(f"Responding with data: {encoded_secret}")
        return jsonify({"your_secret": encoded_secret})
    except SecretNotFound:
        logger.error(f"Secret with id {secret_id} not found")
        return jsonify({"error": f"Secret with id {secret_id} not found"}), 404
    except Exception as e:
        logger.error(e)
        logger.info(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 502


if __name__ == "__main__":
    app.run(host=config.APP_HOST, debug=True)
