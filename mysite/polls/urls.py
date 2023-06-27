from django.urls import path, include

from . import views


app_name = "polls"
urlpatterns = [
	path("", views.IndexView.as_view(), name="index"),
	path("<int:pk>/", views.DetailView.as_view(), name="details"),
	path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
	path("<int:poll_id>/vote/", views.vote, name="vote"),

    path("__debug__/", include("debug_toolbar.urls")),

    path('api/', include('rest_framework.urls')),

    path('api/polls/', views.PollList.as_view(), name='poll-list'),
    path('api/polls/<int:pk>/', views.PollDetail.as_view(), name='poll-detail'),
 	path('api/answers/', views.AnswerCreate.as_view(), name='answer-create'),
 	path('api/polls/<int:pk>/questions/', views.QuestionList.as_view(), name="question-list")
]