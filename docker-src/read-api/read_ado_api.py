from operator import index
from flask import Flask, request, jsonify, abort
import datetime
import database
import time
from flask_cors import CORS, cross_origin

read_service = Flask(__name__)
cors = CORS(read_service)
read_service.config['CORS_HEADERS'] = 'Content-Type'

@read_service.route("/")
@cross_origin()
def welcome():
    return "Welcome ADOs, please access /read to find information on an athlete"


@read_service.route("/read", methods=["GET"])
@cross_origin()
def getAthleteInfo():
    ado_requestinfo = request.get_json(force=True)
    ado_username = ado_requestinfo["ADO_email"]
    athlete_email = ado_requestinfo["Athlete_email"]

    athlete_info = database.db.athlete.find_one({"email": athlete_email})
    if athlete_info is None:
        abort(404)
    return_avails = {}
    ind = 0
    for item in athlete_info["availability"]:
        # print(athlete_info["availability"][item])
        item["time_slot_start"] = time.mktime(
            datetime.datetime.strptime(
                item["time_slot_start"], "%Y-%m-%d %H:%M:%S"
            ).timetuple()
        )
        item["time_slot_end"] = time.mktime(
            datetime.datetime.strptime(
                item["time_slot_end"], "%Y-%m-%d %H:%M:%S"
            ).timetuple()
        )

        if item["time_slot_start"] > time.time():
            return_avails[ind] = item
            ind += 1

    if athlete_info["ado_email"] != ado_username:
        return "Access to athlete information not allowed"
    else:
        return jsonify(return_avails)
        # return return_avails


if __name__ == "__main__":
    read_service.run(host="0.0.0.0", debug=True)
