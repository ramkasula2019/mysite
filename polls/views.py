from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Question, Choice
from django.template import loader
from django.urls import reverse

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
    question = get_object_or_404(Question, pk = question_id)
    return render(requests,'polls/results.html', {'question':question})

def vote(requests, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=requests.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(requests, 'polls/detail.html', 
        {'question':question, 'error_message' : 'you didnot select a choice',})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))

