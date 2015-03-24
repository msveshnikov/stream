# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from stream.models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(p.id,)))


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def hello(request):
    return HttpResponse("Здравствуй, Мир")


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)


def poll(request):
    new = request.POST['new']
    q = Question(question_text=new, pub_date=timezone.now())
    q.save()
    return HttpResponseRedirect('/')
