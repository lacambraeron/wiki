from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("save_entry/", views.save_entry, name="save_entry"),
    path("random_entry_view/", views.random_entry_view, name="random_entry_view"),
    path("<str:title>/", views.display_content, name="entry"),
    path("edit/<str:title>", views.edit, name="edit")
]