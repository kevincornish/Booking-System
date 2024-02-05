from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import generic

def index(request):
    return render(request, "index.html",{})

def logout_view(request):
    logout(request)
    return redirect('home')

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'