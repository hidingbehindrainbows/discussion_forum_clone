from django.urls import path
from .views import ChatPage

urlpatterns = [
    path("", ChatPage.as_view(), name="livechat"),    
]

# from django.urls import path, include
# from .views import ChatPage
 
 
# urlpatterns = [
#     path("", ChatPage, name="livechat"),
# ]

# from django.urls import path

# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<str:room_name>/', views.room, name='room'),
# ]