from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.article_search, name="search"),
    path("newpage/", views.create_new, name="newpage"),
    path("random", views.random, name="random"),
    path("<str:entry_name>/", views.entry, name="entry"),
    path("<str:entry_name>/edit", views.edit, name="edit"),
]
