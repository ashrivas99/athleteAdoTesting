from flask import Flask
from pymongo import MongoClient
from login import login_service

CONNECTION_STRING = "mongodb+srv://dbuser:password0@cluster0.8ehbg.mongodb.net/main?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)
db = client.main
