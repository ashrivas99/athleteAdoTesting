import redis
from redis.cluster import RedisCluster as Redis
import json
import datetime

def athleteAvailability(user_id, location_coordinates, start_datetime, submission_datetime, redis_client):
    athlete_info_dict = {'location_coordinates': location_coordinates,
                          'start_datetime': start_datetime,
                          'submission_datetime': submission_datetime,}
    redis_client.set(user_id, json.dumps(athlete_info_dict))

def append_athleteAvailability(user_id, location_coordinates, start_datetime, submission_datetime, redis_client):
    athlete_info_dict = {'location_coordinates': location_coordinates,
                          'start_datetime': start_datetime,
                          'submission_datetime': submission_datetime,}
    redis_client.append(user_id, json.dumps(athlete_info_dict))

# Makes connection to redis db
redis_client = Redis(host='localhost', port=7000)

# Athlete writes availability
user_id = "id507351348x_2"
location_coordinates = {'Lat': 53.33, 'Long': -6.30}
start_datetime = ['2022-04-16 17:00']
submission_datetime = str(datetime.datetime.now())

#append_athleteAvailability(user_id, location_coordinates, start_datetime, submission_datetime, redis_client)
#redis_client.append(user_id, json.dumps({"location_coordinates": {"Lat": 53.33, "Long": -6.3}, "start_datetime": ["2022-04-16 17:00"], "submission_datetime": "2022-04-13 13:53:54.744145"}))

athlete_available = redis_client.get(user_id)
print(athlete_available)
