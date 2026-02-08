from django.urls import path
from . import views

urlpatterns = [
    path("clients/create/", views.create_client),
    path("projects/create/", views.create_project),
    path("projects/", views.list_projects),
    path("assignments/create/", views.assign_collaborator),
]