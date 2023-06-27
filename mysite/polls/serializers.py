from rest_framework import serializers
from django.core.cache import cache

from .models import Poll, Choice, Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
	choices = AnswerSerializer(many=True, read_only=True)
	answer_count = serializers.SerializerMethodField()

	def get_answer_count(self, choice):
		cache_key = f'answer_count_{choice.pk}'
		answer_count = cache.get(cache_key)
		if answer_count is None:
			answer_count = choice.answer_set.count()
			cache.set(cache_key, answer_count)
		return answer_count

	class Meta:
		model = Choice
		fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
	choices = ChoiceSerializer(many=True, read_only=True)
	class Meta:
		model = Question
		fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'

