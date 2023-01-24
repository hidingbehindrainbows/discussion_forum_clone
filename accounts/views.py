from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from threads.models import Profile
from django.shortcuts import get_object_or_404
from .forms import ProfilePageForm

# Create your views here.

class CreateUserProfilePageView(LoginRequiredMixin, CreateView):
    model = Profile
    # form_class = ProfilePageForm
    template_name= "registration/create_user_profile_page.html"
    fields = ("bio", "pfp")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ShowProfilePageView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "registration/profile.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        current_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        
        context["current_user"] = current_user
        return context
    

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class EditSettingsView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = "registration/edit_settings.html"
    success_url = reverse_lazy("home")
    
    def get_object(self):
        return self.request.user

class EditUserPageView(UpdateView):
    model = Profile
    template_name = "registration/edit_profile_page.html"
    fields = ["bio", "pfp"]
