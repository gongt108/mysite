from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import os
from datetime import datetime
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv

client = MongoClient(os.getenv("MONGO_URI"))
db = client["mysite"]
print(db.list_collection_names())

# db.polls_question.insert_one(
#     {"question_text": "what is your favorite color?", "pub_date": datetime.now()}
# )

print(
    "new polls question",
    db.polls_question.find_one({"_id": ObjectId("65bea35cca2306345c688e27")}),
)


# Create your views here.
def index(request):
    return HttpResponse("Hello world. You are in polls.")
