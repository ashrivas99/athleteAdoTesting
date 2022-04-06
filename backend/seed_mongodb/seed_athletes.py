from faker import Factory
import db
from dummy_data_generated.country_list import COUNTRY_LIST
from dummy_data_generated.data_ado_email_password import ADO_EMAIL_PASS
import time, random, json
import datetime

athlete_email_password_ado_dict = {}
ado_emails = list(ADO_EMAIL_PASS.keys())


def store_athlete_data():
    with open("data_athlete_email_pass_adoEmail.py", "w") as outfile:
        json.dump(athlete_email_password_ado_dict, outfile)


def seed_athlete_collection(fake):
    for i in range(10000):
        gen_athlete_email = fake.email()
        gen_athlete_password = fake.password()
        gen_ado_email = random.choice(ado_emails)

        gen_time_1_start = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=i)
        gen_time_1_end = gen_time_1_start + datetime.timedelta(hours=2)

        gen_time_2_start = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=i + 1)
        gen_time_2_end = gen_time_2_start + datetime.timedelta(hours=3)

        if gen_athlete_email not in athlete_email_password_ado_dict:
            athlete_email_password_ado_dict[gen_athlete_email] = {
                "password": gen_athlete_password,
                "ado_email": gen_ado_email,
            }

            result = db.db.athlete.insert_one(
                {
                    "email": gen_athlete_email,
                    "password": gen_athlete_password,
                    "ado_email": gen_ado_email,
                    "phone": fake.phone_number(),
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "availability": [
                        {
                            "time_slot_start": gen_time_1_start.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "time_slot_end": gen_time_1_end.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "location": {
                                "lat": str(fake.latitude()),
                                "lng": str(fake.longitude()),
                            },
                        },
                        {
                            "time_slot_start": gen_time_2_start.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "time_slot_end": gen_time_2_end.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "location": {
                                "lat": str(fake.latitude()),
                                "lng": str(fake.longitude()),
                            },
                        },
                    ],
                }
            )

            print(f"Inserted {result.inserted_id} at iteration {i}")

    store_athlete_data()


if __name__ == "__main__":
    fake = Factory.create()
    seed_athlete_collection(fake)
