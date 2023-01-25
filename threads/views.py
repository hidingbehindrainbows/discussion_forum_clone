from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # new
from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .forms import CommentForm, ThreadForm
from .models import Thread, Likes, Dislikes, Category
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count


class ThreadView(LoginRequiredMixin, ListView):  # defines the page that shows our threads, it does this by using ListView, which generates an iterable variable
    model = Thread
    template_name = "thread_list.html"
    

class CommentGet(DetailView):  # GETting the comment info
    model = Thread
    template_name = "thread_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):  # POSTing the comment info 
    model = Thread
    form_class = CommentForm
    template_name = "thread_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.thread = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        thread = self.get_object()
        return reverse("thread_detail", kwargs={"pk": thread.pk})


class ThreadDetailView(LoginRequiredMixin, View):  # A wrap view that uses both CommentGet and CommentPost
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ThreadEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # allows users to edit their threads
    model = Thread
    fields = (
        "title",
        "body",
    )
    template_name = "thread_edit.html"

    def test_func(self):  
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser #allow superuser and user to update thread.


class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # allows them to delete their threads
    model = Thread
    template_name = "thread_delete.html"
    success_url = reverse_lazy("thread_list")

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser #Allow superuser to delete thread.


class ThreadCreateView(LoginRequiredMixin, CreateView):  # allows users to create new threads
    model = Thread
    template_name = "thread_new.html"
    form_class= ThreadForm

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required(login_url="login")
def thread_view(request):
    # qs = Thread.objects.annotate(like_count=(Count('liked')-Count('dislike'))).order_by('-like_count')  # has a small error idk why
    qs = Thread.objects.all()
    user = request.user
    context = {
        "qs":qs,
        "user":user,
    }
    return render(request, "thread_list.html", context)


def like_thread(request):
    try:
        user = request.user
        if request.method == "POST":
            thread_id = request.POST.get("thread_id")
            thread_obj = Thread.objects.get(id=thread_id)
            
            if user in thread_obj.liked.all():
                thread_obj.liked.remove(user)
            else:
                thread_obj.liked.add(user)
            like, created = Likes.objects.get_or_create(user=user, thread_id=thread_id)
            
            if not created:
                if like.value == 'Like':
                    like.value = "Unlike"
                else:
                    like.value = "Like"
                    
            like.save()
        return redirect("thread_detail", pk= thread_id)
    except:
        return HttpResponseRedirect(reverse_lazy("thread_detail", kwargs={"pk": thread_id}))

def dislike_thread(request):
    try:
        user = request.user
        if request.method == "POST":
            thread_d_id = request.POST.get("thread_id")
            thread_obj = Thread.objects.get(id=thread_d_id)
            
            if user in thread_obj.dislike.all():
                thread_obj.dislike.remove(user)
            else:
                thread_obj.dislike.add(user)
            dislike, created = Dislikes.objects.get_or_create(user=user, thread_d_id=thread_d_id)
            
            if not created:
                if dislike.value == 'Dislike':
                    dislike.value = "Undo"
                else:
                    dislike.value = "Dislike"
                    
            dislike.save()
        return redirect("thread_detail", pk= thread_d_id)
    except:
        return HttpResponseRedirect(reverse_lazy("thread_detail", kwargs={"pk": thread_d_id}))



def CategoryView(request, cats):
    choices = Category.objects.all().values_list("name")
    all_cats = [item for items in choices for item in items]
    cats = cats.replace("-", " ")
    if cats in all_cats:
        cat_posts = Thread.objects.filter(category=cats)
        return render(request, "categories.html", {"cats":cats, "cat_posts":cat_posts,})
    return redirect("home")

def search_result(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        result = Thread.objects.filter(title__contains=searched).annotate(like_count=(Count('liked')-Count('dislike'))).order_by('-like_count')
        return render(request, "search/search_result.html", {"searched":searched, "result":result})
    return render(request, "search/search_result.html", {})

def watch_thread(request):
    try:
        user = request.user
        if request.method == "POST":
            thread_id = request.POST.get("thread_id")
            thread_obj = Thread.objects.get(id=thread_id)
            
            if user in thread_obj.watched.all():
                thread_obj.watched.remove(user)
            else:
                thread_obj.watched.add(user)
            like, created = Likes.objects.get_or_create(user=user, thread_id=thread_id)
            
            if not created:
                if like.value == 'Watch':
                    like.value = "Unwatch"
                else:
                    like.value = "Watch"
                    
            like.save()
        return redirect("thread_detail", pk= thread_id)
    except:
        return HttpResponseRedirect(reverse_lazy("thread_detail", kwargs={"pk": thread_id}))

