# views.py
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import User, UserProfile
from .forms import UserProfileForm


def create_user(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = UserProfileForm()

    return render(request, 'users/add_user.html', {'form': form})


def users(request):
    users = User.objects.all()
    return render(request, 'users/users.html', {'users': users})
