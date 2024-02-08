from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from pymongo import MongoClient
import os
from datetime import datetime, timedelta
from bson import ObjectId
from dotenv import load_dotenv
from .models import Choice, Question

load_dotenv

client = MongoClient(os.getenv("MONGO_URI"))
db = client["mysite"]
# print(db.list_collection_names())

# print("----Availiable Collections----")
# for collection in db.list_collection_names():
#     print("---> " + collection)
# print("")
# print("----Availiable Questions----")
# all_questions = db.polls_question.find()
# q_num = 1
# for q in all_questions:
#     print(q)
#     q_num += 1
# print("")

# new_q = {"question_text": "What's new?", "pub_date": datetime.now()}
# for q in db.polls_question.find():
#     if q["question_text"] == new_q["question_text"]:
#         does_new_q_exist_in_db = True
#         break
# if not does_new_q_exist_in_db:
#     db.polls_question.insert_one(new_q)
#     print("New question added to the database!")
# else:
#     print("Question already exists in the database!")
# print("")

# db.polls_question.insert_one(
#     {"question_text": "what is your favorite color?", "pub_date": datetime.now()}
# )

# print(
#     "new polls question",
#     db.polls_question.find_one({"_id": ObjectId("65bea35cca2306345c688e27")}),
# )
# # TODO Search by question_text
# print(
#     "Search by question_text",
#     db.polls_question.find_one({"question_text": "what is your favorite color?"}),
# )
# # TODO Search a question by a certain text
# question = (
#     db.polls_question.find_one({"question_text": {"$regex": "what", "$options": "i"}}),
# )

# print("Search by a certain text", question)

# # TODO Search all question by one date
# target_date = datetime(2024, 2, 3)
# # Find questions with the specified date
# found_questions = db.polls_question.find(
#     {"pub_date": {"$gte": target_date, "$lt": target_date + timedelta(days=1)}}
# )

# # Print or iterate over the found questions
# print("----Find questions with the specified date-----")
# for question in found_questions:
#     print(question)


# TODO Update a question (pub_date -> needs to be set to current date)
# found_question = db.polls_question.find_one(
#     {"pub_date": {"$gte": target_date, "$lt": target_date + timedelta(days=1)}}
# )
# print("before change", found_question)
# today_date = datetime.now()
# result = db.polls_question.find_one_and_update(
#     {"pub_date": {"$gte": target_date, "$lt": target_date + timedelta(days=1)}},
#     {"$set": {"pub_date": today_date}},
#     return_document=True,
# )
# print("after", result)

# TODO Delete a question
# db.polls_question.find_one_and_delete({"_id": ObjectId("65bb3ae3e5bdf5ff9fc62e5f")})
# db.polls_question.find_one({"_id": ObjectId("65bb3ae3e5bdf5ff9fc62e5f")})


# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
