import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Poll(models.Model):
	poll_title = models.CharField(max_length=200)
	pub_date = models.DateTimeField("date published")
	def __str__(self): 
		return self.poll_title


class Question(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField("date published")
	def __str__(self):
		return self.question_text

	@admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
	def was_published_recently(self):
		# return self.pub_date >= timezone.now() - datetime.timedelta(days=1)	
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
	question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)	
	def __str__(self):
		return self.choice_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)