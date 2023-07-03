from django.urls import path
from .models import Profile
from .views import HomePageView, AboutPageView

urlpatterns = [
    path("profile/", Profile.as_view(), name="profile"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("", HomePageView.as_view(), name="home"),
]
