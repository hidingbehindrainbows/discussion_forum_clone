from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # new
from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .forms import CommentForm
from .models import Thread


class ThreadView(LoginRequiredMixin, ListView):  # defines the page that shows our threads, it does this by using ListView, which generates an iterable variable
    model = Thread
    template_name = "thread_list.html"
    
    # def get_queryset(self):
    #     return self.model.objects.filter(thread=self.kwargs['pk'])

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


class ThreadEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # allows ysers to edit their threads
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
    fields = ("title", "body")  # new

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)