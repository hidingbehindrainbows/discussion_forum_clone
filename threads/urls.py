from django.urls import path

from .views import (
    ThreadView,
    ThreadDetailView,
    ThreadEditView,
    ThreadDeleteView,
    ThreadCreateView,  # new
)

urlpatterns = [
    path("<int:pk>/", ThreadDetailView.as_view(), name="thread_detail"),
    path("<int:pk>/edit/", ThreadEditView.as_view(), name="thread_edit"),
    path("<int:pk>/delete/", ThreadDeleteView.as_view(), name="thread_delete"),
    path("new/", ThreadCreateView.as_view(), name="thread_new"),  # new
    path("", ThreadView.as_view(), name="thread_list"),
]