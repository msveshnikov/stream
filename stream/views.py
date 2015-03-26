# -*- coding: utf-8 -*-
import datetime
import urllib.request

from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import RequestContext, loader
import bs4

from stream.models import Question, Choice


class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'


def index(request):
    pic_list = Question.objects.order_by('-pub_date')  # .values('question_text').distinct()
    paginator = Paginator(pic_list, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        pics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pics = paginator.page(paginator.num_pages)
    template = loader.get_template('index.html')
    context = RequestContext(request, {'pics': pics})
    return HttpResponse(template.render(context))


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


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)


def poll(request):
    a = request.POST['new']
    if a[-3:] == "jpg" or a[-3:] == "gif" or \
                    a[-3:] == "png" or a[-4:] == "jpeg" or "youtube" in a or "vimeo" in a:
        q = Question(question_text=a, pub_date=timezone.now())
    else:
        page = urllib.request.urlopen(a).read()  # .decode("utf-8")
        # Get the content of all the elements in the page.
        text = bs4.BeautifulSoup(page).getText(separator=" ")
        # Limit the content to the first 150 bytes, eliminate leading or
        # trailing whitespace.
        snippet = text[0:150]
        # If text was longer than this (most likely), also add '...'
        if len(text) > 150:
            snippet += "..."
        q = Question(question_text=a, pub_date=timezone.now(), question_desc=snippet)
    q.save()
    return HttpResponseRedirect('/')
