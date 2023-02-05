from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from django.db.models import Q
from .models import Message
from accounts.models import CustomUser
# from threads.models import Profile
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.humanize.templatetags.humanize import naturaltime
# Create your views here.


@login_required(login_url="login")
def NewConversation(request, u_id):
    from_user = request.user
    to_user = get_object_or_404(CustomUser, id = u_id)
    body = "Started a new conversation"
    if from_user != to_user:
        try:
            Message.objects.create(user=from_user, sender=from_user, recipient = to_user, body=body)
        except:
            pass
        return redirect("message_inbox")


@login_required(login_url="login")
def Message_inbox(request):
    p = Paginator(Message.get_message(recipient=request.user), 25) #TODO changable
    page = request.GET.get("page")
    page_of_message = p.get_page(page)
    context = {
        "messages": page_of_message,
    }
    return render(request, "messages/message_inbox.html", context)

def SendMessages(request):
    from_user = request.user
    to_user_id = request.POST.get("to_user_id")
    body = request.POST.get("body")
    
    if request.method == "POST":
        to_user = get_object_or_404(CustomUser, id = to_user_id)
        Message.send_message(from_user, to_user, body)
        return HttpResponseRedirect(reverse("directs", args=to_user_id))
    else:
        return HttpResponseBadRequest()

def LoadMore(request):
    user = request.user
    if is_ajax(request):
        pk = request.POST.get('u_id')
        page_number_directs = request.POST.get('page')
        print(page_number_directs)

        directs = Message.objects.filter(user=user, recipient__id=pk).order_by('-date').values(
            'sender__profile__pfp',
            'sender__first_name',
            'sender__last_name',
            'body',
            'date',
        )

        #Pagination for directs
        p = Paginator(directs, 3)

        if p.num_pages >= int(page_number_directs):
            directs_data = p.get_page(page_number_directs)
            print(directs_data, "second", sep=", ")

            #Creating the list of data
            directs_list = list(directs_data)

            for x in range(len(directs_list)):
                directs_list[x]['date'] = naturaltime(directs_list[x]['date'])
            
            return JsonResponse(directs_list, safe=False)
            # return HttpResponseBadRequest
        else:
            return JsonResponse({'empty': True}, safe=False)
            # return HttpResponseBadRequest


def Directs(request, pk):
    user = request.user
    messages = Message.get_message(user=request.user)
    directs = Message.objects.filter(user=user, recipient__id=pk).order_by('-date')
    directs.update(is_read=True)
    for message in messages:
        if message['recipient'].id==pk:
            message['unread'] = 0

    #Pagination for directs
    p = Paginator(directs, 3)
    page = request.GET.get('page')
    directs_data = p.get_page(page)
    
    context = {
        'directs': directs_data,
        'messages': messages,
        'active_direct': pk
    }

    return render(request, 'messages/directs.html', context)



def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'