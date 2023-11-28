from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q

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


class CreateUser(CreateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/add_user.html'

    def get_success_url(self):
        return reverse('users')


class MembersListView(ListView):
    template_name = 'users/members.html'
    context_object_name = 'members'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        members = User.objects.all().order_by('-id')

        if query:
            members = members.filter(
                Q(phone_number__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return members


class UserDetail(DetailView):
    model = User
    template_name = 'users/member.html'
