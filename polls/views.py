# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, Http404
from .models import Question, Choice
from django.db.models import F
from django.template import RequestContext, loader, Template, Context
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import (
    render, render_to_response, get_object_or_404, get_list_or_404
)
from django.utils import timezone

#from django.views.decorators.csrf import csrf_protect

# # Create your views here.
# def index(request):
#     q_list = Question.objects.order_by('-pub_date')[:3]
#     #res = ','.join(p.question_text for p in q_list)
#     template = loader.get_template('polls/index.html')
#     # context = RequestContext(request, {
#     #     'q_list': q_list,
#     # })
#
#     return HttpResponse(render(request, 'polls/index.html', {'q_list': q_list}))
# #@csrf_protect
# def detail(request, question_id):
#     # question = Question.objects.get(id=question_id)
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Qeustion does not exist!")
#     question = get_object_or_404(Question, pk=question_id)
#     #template = loader.get_template('polls/details.html')
#     template = get_template('polls/details.html')
#     #context = RequestContext(request, {"question":question})
#     context = {"question":question}
#     #print(request.POST)
#     #return HttpResponse(render(request, "polls/details.html", {"question":question}))
#     return HttpResponse(template.render(request=request, context=context))
#
# def results(request, question_id):
#     #questions = get_list_or_404(Question, question__id__gt = F(question_id))
#     print('results called')
#     question = get_object_or_404(Question, pk=question_id)
#     return HttpResponse(render(request, 'polls/results.html', {'question':question}))
#
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        print('debug except  *****')
        return render(request, 'polls/details.html', {
            'question':p,
            'error_message':'you didnot selcet a choice',
        })
    else:
        select_choice.votes += 1
        select_choice.save()
        #print(reverse('polls:polls_results'))
        return HttpResponseRedirect(reverse('polls:polls_results', args=(p.id,)))

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #return Question.objects.order_by('-pub_date')[:5]
        if Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] == []:
            return HttpResponse("No polls are available")
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    template_name = "polls/details.html"
    model = Question
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
