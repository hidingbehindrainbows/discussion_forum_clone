from django.urls import path

from .views import (
    ThreadDetailView,
    ThreadEditView,
    ThreadDeleteView,
    ThreadCreateView,  # new
    thread_view,
    like_thread,
    dislike_thread,
    CategoryView,
    search_result,
)

urlpatterns = [
    path("<int:pk>/", ThreadDetailView.as_view(), name="thread_detail"),
    path("<int:pk>/edit/", ThreadEditView.as_view(), name="thread_edit"),
    path("<int:pk>/delete/", ThreadDeleteView.as_view(), name="thread_delete"),
    path("new/", ThreadCreateView.as_view(), name="thread_new"),  # new
    path("", thread_view, name="thread_list"),
    path("like/", like_thread, name="like_thread"),
    path("dislike/", dislike_thread, name="dislike_thread"),
    path("category/<str:cats>/", CategoryView, name="category" ),
    path("search_result", search_result, name="search_result" ),
]