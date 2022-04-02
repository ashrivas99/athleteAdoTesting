from pymongo import MongoClient
from random import randint

# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB
client = MongoClient(
    "mongodb+srv://dbuser:password0@cluster0.8ehbg.mongodb.net/main?retryWrites=true&w=majority"
)

db = client.business

fivestar = db.reviews.find_one({"rating": 5})
print(fivestar)
