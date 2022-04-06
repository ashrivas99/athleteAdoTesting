from flask import Flask
import database

login_service = Flask(__name__)


@login_service.route("/")
def welcome():
    return "welcome to login service"


@login_service.route("/login")
def login():
    return "login"


# test to read data from the data base
@login_service.route("/test")
def test():
    user1 = database.db.athlete.find_one({"email": "ashrivas@tcd.ie"})
    return f"{user1.get('email')}"


if __name__ == "__main__":
    login_service.run(debug=True)
