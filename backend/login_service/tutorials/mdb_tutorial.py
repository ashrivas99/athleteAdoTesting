from pymongo import MongoClient

# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB
client = MongoClient(
    "mongodb+srv://dbuser:password0@cluster0.8ehbg.mongodb.net/main?retryWrites=true&w=majority"
)
db = client.main
# print(db)
# Issue the serverStatus command and print the results
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)
