from flask import Flask, request, jsonify, abort
import database
import redis
from flask_cors import CORS, cross_origin



login_service = Flask(__name__)

cors = CORS(login_service)
login_service.config['CORS_HEADERS'] = 'Content-Type'


@login_service.route("/")
@cross_origin()
def welcome():
    return "welcome to login service. To login for athletes please use /loginAthlete, for ado's please use /loginAdo"


@login_service.route("/loginAthlete", methods=["POST"])
@cross_origin()
def loginAthlete():
    athlete_login_info = request.get_json(force=True)
    athlete_username = athlete_login_info["email"]
    athlete_password = athlete_login_info["password"]
   
    redis_client = redis.Redis(host='localhost', port=6379)
    athlete_db_login_info_password = redis_client.get(athlete_username)
 
    if athlete_db_login_info_password is None:
        print("checking database")
        athlete_db_login_info = database.db.athlete.find_one({"email": athlete_username})
        if athlete_db_login_info is None:
            # Return boolean false and error 404
            return jsonify(False), 404
        athlete_db_login_info_password = athlete_db_login_info["password"]
        redis_client.set(athlete_username, athlete_db_login_info_password)
    
    else :
        athlete_db_login_info_password = athlete_db_login_info_password.decode("utf-8")

    if athlete_password == athlete_db_login_info_password:
        return jsonify(True), 200
    else:
        return jsonify({"message": "Wrong password"}), 401


@login_service.route("/loginAdo", methods=["POST"])
@cross_origin()
def loginAdo():
    ado_login_info = request.get_json(force=True)
    ado_username = ado_login_info["email"]
    ado_password = ado_login_info["password"]

    ado_db_login_info = database.db.ado.find_one({"email": ado_username})

    if ado_db_login_info is None:
        return jsonify(False), 404

    ado_db_login_info_password = ado_db_login_info["password"]

    if ado_password == ado_db_login_info_password:
        return jsonify(True), 200
    else:
        return jsonify({"message": "Wrong password"}), 401


if __name__ == "__main__":
    login_service.run(host="0.0.0.0", debug=True)
