from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from rest_framework import generics

from .models import Question, Choice, Poll, Answer
from .serializers import PollSerializer, AnswerSerializer, QuestionSerializer


# def index(request): 
	# return HttpResponse("Hola, world! You are at the polls index.")

# def index(request):
# 	latest_question_list = Question.objects.order_by("-pub_date")[:5]
# 	output = ", ".join([q.question_text for q in latest_question_list])
# 	return HttpResponse(output)

# def index(request):
# 	latest_question_list = Question.objects.order_by("-pub_date")[:5]
# 	template = loader.get_template("polls/index.html")
# 	context = {
# 		"latest_question_list": latest_question_list,
# 	}
# 	return HttpResponse(template.render(context, request))


# def index(request):
# 	latest_question_list = Question.objects.order_by("-pub_date")[:5]
# 	context = {
# 		"latest_question_list": latest_question_list,
# 	}
# 	return render(request, "polls/index.html", context)

class IndexView(generic.ListView):
	template_name = "polls/index.html"
	context_object_name = "latest_poll_list"

	def get_queryset(self):
		"""Return last 5 published questions."""
		# return Question.objects.order_by("-pub_date")[:5]
		# return Poll.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
		return Poll.objects.all()[:5]	

# def detail(request, question_id):
# 	return HttpResponse("Detail of Question #%s" % question_id)

# def detail(request, question_id):
# 	try:
# 		question = Question.objects.get(pk=question_id)
# 	except Question.DoesNotExist:
# 		raise Http404("Question does not exist.")
# 	return render(request, "polls/detail.html", {"question": question})	

# def detail(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, "polls/detail.html", {"question": question})	

class DetailView(generic.DetailView):
	model = Poll
	template_name = "polls/detail.html"

	# def get_queryset(self):
	# 	"""
	# 	Excludes any questions that aren't published yet.
	# 	"""
	# 	return Poll.objects.filter(pub_date__lte=timezone.now())

# def results(request, question_id):
#  	response = "Results of Question #%s"
#  	return HttpResponse(response % question_id)

# def results(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, "polls/results.html", {"question": question})

class ResultsView(generic.DetailView):
	model = Poll
	template_name = "polls/results.html"

# def vote(request, question_id):
# 	return HttpResponse("Votes of Question #%s" % question_id)

def vote(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	questions = Question.objects.filter(poll=poll)
	
	for question in questions:
		try:
			selected_choice = question.choices.get(pk=request.POST['{}'.format(question.id)])
	# question = get_object_or_404(Question, pk=question_id)
	# try:
		# selected_choice = question.choice_set.get(pk=request.POST["choice"])
		except (KeyError, Choice.DoesNotExist):
			return render(request, "polls/detail.html", {
				"poll": poll,
				"error_message": "You did not select a choice."
			})	
	
		Answer.objects.create(question=question, choice=selected_choice)
		# selected_choice.votes += 1
		# selected_choice.save()
	return HttpResponseRedirect(reverse("polls:results", args=(poll.id,)))	

# API

class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_url_kwarg = 'pk'

class AnswerCreate(generics.CreateAPIView):
    serializer_class = AnswerSerializer

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.filter()
    serializer_class = QuestionSerializer
    lookup_field = 'poll'