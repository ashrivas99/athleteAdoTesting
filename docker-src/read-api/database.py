from flask import Flask
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://dbuser:password0@cluster1.8ehbg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)
db = client.main
