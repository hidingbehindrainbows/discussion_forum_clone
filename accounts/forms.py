from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django import forms
from threads.models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "USN",
            "email",
        )
        
class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = CustomUser
        fields = ("username", "USN", "first_name", "last_name","email",)

class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "pfp")