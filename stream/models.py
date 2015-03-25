import datetime
import re

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):  # __unicode__ on Python 2
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.choice_text


class Import(object):
    def do(self):
        with open("c:\\version.txt") as f:
            mystring = f.read()
        mystring_list = [item for item in mystring.split(" ")]
        for item in mystring_list:
            try:
                a = re.search("(?P<url>https?://[^\s]+)", item).group("url")
                if (a[-3:] == "jpg" or a[-3:] == "gif"):
                    print(a)
                    q = Question(question_text=a, pub_date=timezone.now())
                    q.save()
            except:
                pass