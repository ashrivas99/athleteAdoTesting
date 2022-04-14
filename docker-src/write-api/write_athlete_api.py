from flask import Flask, request, jsonify, abort
import database
from datetime import datetime, timedelta
import pandas as pd
from pprint import pprint

write_service = Flask(__name__)


@write_service.route("/")
def welcome():
    return "welcome to the write service for athletes"


def check_cutoff_time(time_slot_start):
    time_slot_start_datetime = datetime.fromtimestamp(time_slot_start / 1e3)
    cutoff_time = datetime.now() + timedelta(days=2)

    cutoff_time_satisfied = True if time_slot_start_datetime > cutoff_time else False
    return cutoff_time_satisfied


def check_timeslot_gt_one_hour(time_slot_start, time_slot_end):
    time_slot_start_pd = pd.to_datetime(time_slot_start, utc=True, unit="ms")
    time_slot_end_pd = pd.to_datetime(time_slot_end, utc=True, unit="ms")
    time_slot_duration = time_slot_end_pd - time_slot_start_pd

    time_slot_duration_in_hours = time_slot_duration.total_seconds() / 3600
    time_slot_gt_one_hour = True if time_slot_duration_in_hours >= 1 else False

    print("time_slot_duration_in_hours: ", time_slot_duration_in_hours)
    return time_slot_gt_one_hour


@write_service.route("/writeAvailability", methods=["POST"])
def writeAvailability():
    athlete_availability_info = request.get_json(force=True)
    athlete_email = athlete_availability_info["email"]
    athlete_availability_list = athlete_availability_info["availability"]

    athlete_db_email = database.db.athlete.find_one({"email": athlete_email})

    if athlete_db_email is None:
        return jsonify({"message": "athlete not found"}), 404

    # get _id from athlete_availability_info
    athlete_availability_info_id = athlete_db_email.get("_id")

    for idx, athlete_availability in enumerate(athlete_availability_list):
        time_slot_start = athlete_availability["datetime_start"]
        time_slot_end = athlete_availability["datetime_end"]

        # validate cutoff time
        cutoff_satisfied = check_cutoff_time(time_slot_start)

        if not cutoff_satisfied:
            return (
                jsonify(
                    {
                        "message": "timeslot is past cutoff",
                        "timeslot_failed": athlete_availability_list[idx],
                    }
                ),
                400,
            )

        # validate timeslot is greater than one hour
        time_slot_constraint_satisfied = check_timeslot_gt_one_hour(
            time_slot_start, time_slot_end
        )

        if not time_slot_constraint_satisfied:
            return (
                jsonify(
                    {
                        "message": "timeslot is less than one hour",
                        "timeslot_failed": athlete_availability_list[idx],
                    }
                ),
                400,
            )

        time_slot_start_str = datetime.fromtimestamp(time_slot_start / 1e3).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        time_slot_end_str = datetime.fromtimestamp(time_slot_end / 1e3).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

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
                    "_id": athlete_availability_info_id,
                    "availability.time_slot_start": time_slot_start_str,
                },
                {"$set": {"availability.$": athlete_availability_object}},
            )
        else:
            print("no existing availability found, adding new availability")
            database.db.athlete.update_one(
                {"_id": athlete_availability_info_id},
                {"$push": {"availability": athlete_availability_object}},
            )

    return jsonify({"message": "athlete availability added"}), 200


if __name__ == "__main__":
    write_service.run(host="0.0.0.0", debug=True)
