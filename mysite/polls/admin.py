from django.contrib import admin

from .models import Question, Choice, Poll

class ChoiceInLine(admin.TabularInline):
	model = Choice
	extra = 3

class QuestionInLine(admin.TabularInline):
	model = Question
	extra = 3
	fieldsets = [
		(None, {"fields": ["question_text"]}),
		('Date information', {"fields": ["pub_date"], "classes": ["collapse"]}),
	]
	inlines = [ChoiceInLine]
	list_display = ["question_text", "pub_date", "was_published_recently"]
	list_filter = ["pub_date"]

class PollAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {"fields": ["poll_title"]}),
		('Date information', {"fields": ["pub_date"], "classes": ["collapse"]}),
	]
	inlines = [QuestionInLine]

class QuestionAdmin(admin.ModelAdmin):
	model = Question
	extra = 3
	fieldsets = [
		(None, {"fields": ["question_text"]}),
		('Date information', {"fields": ["pub_date"], "classes": ["collapse"]}),
	]
	inlines = [ChoiceInLine]
	list_display = ["question_text", "pub_date", "was_published_recently"]
	list_filter = ["pub_date"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAdmin)
