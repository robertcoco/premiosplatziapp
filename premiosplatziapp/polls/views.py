#python

#djanog
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
# Create your views here.

# def index(request):
#     # ex: /polls/
#     lasted_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "lasted_question_list" : lasted_question_list
#     })
#     # ex: /polls/4
# def detail(request, question_id):
#     question =  get_object_or_404(Question, pk = question_id)
#     return render(request, "polls/detail.html", {
#         "question" : question
#     })
#     # ex: /polls/4/results
# def results(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, "polls/results.html", {
#         "question": question
#     })

class IndexView(generic.ListView):
    template_name = "polls/index.html" 
    context_object_name = "lasted_question_list"

    def get_queryset(self):
        """Return the five last questions of the list"""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    # ex: /polls/4/vote
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try: 
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist): 
        return render(request, "polls/detail.html", {
            "question" : question,
            "error_message" : "Didn't select any choice"
        })
    else :
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args = (question.id,)))