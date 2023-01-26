from django.shortcuts import render, redirect
from .models import Notification
from threads.models import WatchThread

# Create your views here.

def ShowNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(reciever=user).order_by("-date")
    context= {
        "notifications": notifications,
    }
    return render(request, "show_notifications.html", context)

def DeleteNotifications(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, reciever=user).delete()
    return redirect("show_notifications")


def CountNotifications(request):
    count = None
    if request.user.is_authenticated:
        count = Notification.objects.filter(reciever=request.user, is_seen=False).count()
    return { "count_notifications":count }
    