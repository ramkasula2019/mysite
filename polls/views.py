from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from polls.models import Question
from django.template import loader

# Create your views here.
def index (requests):
    latest_question_list = Question.objects.order_by('-pub_date') [:5]
    #output = ','.join(q.question_text for q in latest_question_list)
    #return HttpResponse(output)
    #template = loader.get_template('polls/index.html')
    context = {'latest_question_list':latest_question_list}
    #return HttpResponse(template.render(context, requests))

    return render(requests, 'polls/index.html', context)


def detail(requests, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(requests, 'polls/detail.html', {'question':question})

def results(requests, question_id):
    return HttpResponse(" you are on the result of %s." %question_id)

def vote(requests, question_id):
    return HttpResponse(" you have voted count %s." %question_id)

