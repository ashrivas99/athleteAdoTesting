from faker import Factory
import db, random, json
from dummy_data_generated.country_list import COUNTRY_LIST
from pymongo import errors
import time

ado_email_password_dict = {}


def store_ado_data():
    with open("seed_ado_email_password_ta.json", "w") as outfile:
        json.dump(ado_email_password_dict, outfile)


def seed_ado_collection(fake):
    for i in range(101):
        gen_ado_email = fake.email()
        gen_ado_password = fake.password()

        if gen_ado_email not in ado_email_password_dict:
            ado_email_password_dict[gen_ado_email] = gen_ado_password
            result = db.db.ado.insert_one(
                {
                    "email": gen_ado_email,
                    "password": gen_ado_password,
                    "phone": fake.phone_number(),
                    "country": random.choice(COUNTRY_LIST),
                }
            )

            print(f"Inserted {result.inserted_id} at iteration {i}")

    store_ado_data()


if __name__ == "__main__":
    fake = Factory.create()
    seed_ado_collection(fake)
