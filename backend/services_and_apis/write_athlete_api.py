from flask import Flask, request, jsonify, abort
import database
from pprint import pprint
import datetime

write_service = Flask(__name__)


@write_service.route("/")
def welcome():
    return "welcome to the write service for athletes"


@write_service.route("/writeAvailability", methods=["POST"])
def writeAvailability():
    athlete_availability_info = request.get_json(force=True)
    athlete_email = athlete_availability_info["email"]
    athlete_availability_list = athlete_availability_info["availability"]
    pprint(athlete_availability_list)

    athlete_db_email = database.db.athlete.find_one({"email": athlete_email})

    if athlete_db_email is None:
        return jsonify({"message": "athlete not found"}), 404

    for athlete_availability in athlete_availability_list:
        time_slot_start = athlete_availability["datetime_start"]
        time_slot_end = athlete_availability["datetime_end"]

        # convert to datetime string  in format "YYYY-MM-DD HH:MM:SS" from integer timestamp
        time_slot_start_str = datetime.datetime.fromtimestamp(
            time_slot_start / 1e3
        ).strftime("%Y-%m-%d %H:%M:%S")

        time_slot_end_str = datetime.datetime.fromtimestamp(
            time_slot_end / 1e3
        ).strftime("%Y-%m-%d %H:%M:%S")

        athlete_availability_object = {
            "time_slot_start": time_slot_start_str,
            "time_slot_end": time_slot_end_str,
            "location": {
                "lat": str(athlete_availability["lat"]),
                "lng": str(athlete_availability["lng"]),
            },
        }

        # If the start time slot exists, we will update the end time slot and location
        athlete_availability_db_search = database.db.athlete.find_one(
            {
                "email": athlete_email,
                "availability.time_slot_start": time_slot_start_str,
            }
        )

        if athlete_availability_db_search is not None:
            print("found existing availability, updating the availability")
            database.db.athlete.update_one(
                {
                    "email": athlete_email,
                    "availability.time_slot_start": time_slot_start_str,
                },
                {"$set": {"availability.$": athlete_availability_object}},
            )
        else:
            print("no existing availability found, adding new availability")
            database.db.athlete.update_one(
                {"email": athlete_email},
                {"$push": {"availability": athlete_availability_object}},
            )

    return jsonify({"message": "availability added"}), 200


if __name__ == "__main__":
    write_service.run(debug=True)
