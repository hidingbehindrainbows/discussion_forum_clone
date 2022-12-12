# from django.shortcuts import render, redirect
 
 
# def ChatPage(request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         return redirect("login")
#     context = {}
#     return render(request, "chat\live.html", context)


from django.views.generic import TemplateView
from .models import Chat
class ChatPage(TemplateView):
    model = Chat
    template_name = "chat/live.html"

# from django.shortcuts import render

# from .models import Message

# def index(request):
#     return render(request, 'chat\live.html')

# def room(request, room_name):
#     username = request.GET.get('username', 'Anonymous')
#     messages = Message.objects.filter(room=room_name)[0:25]

#     return render(request, 'chat/live.html', {'room_name': room_name, 'username': username, 'messages': messages})