from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q

from .models import User, UserProfile
from .forms import AttendanceForm, UserProfileForm


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


class MembersListView(View):
    template_name = 'users/members.html'
    context_object_name = 'members'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        members = User.objects.all().order_by('-id')
        now = datetime.now()

        if query:
            members = members.filter(
                Q(phone_number__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        form = AttendanceForm()
        return render(request, self.template_name, {'members': members, 'form': form, 'now': now})

    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST)
        now = datetime.now()
        if form.is_valid():
            form.save(start=now)
            return redirect('users')
        else:
            print('-----------')
            print(form.cleaned_data)
            print(form.errors)
        return render(request, self.template_name, {'members': UserProfile.objects.all(), 'form': form, 'now': now})

class UserDetail(DetailView):
    model = User
    template_name = 'users/member.html'


class MarkAttendanceView(View):
    template_name = 'users/mark_attendance.html'

    def get(self, request, *args, **kwargs):
        form = AttendanceForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mark-attendance')
        return render(request, self.template_name, {'form': form})
