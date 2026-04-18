from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index"),
	       path("AdminLogin", views.AdminLogin, name="AdminLogin"),
	       path("Admin.html", views.Admin, name="Admin"),
	       path("Vote.html", views.Vote, name="Vote"),
	       path("ViewCount", views.ViewCount, name="ViewCount"),	
	       path("CastVote", views.CastVote, name="CastVote"),
	       path("CastVoteAction", views.CastVoteAction, name="CastVoteAction"),
	       path("ViewCountAction", views.ViewCountAction, name="ViewCountAction"),
]