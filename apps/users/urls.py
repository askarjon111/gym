from django.urls import path
from apps.users.views import (CreateUser, MembersListView, UserDetail,
                              UserRegistrationView, login_view, LogOutView, UserUpdateView, StaffListView)


urlpatterns = [
    path('', MembersListView.as_view(), name="users"),
    path('staff/', StaffListView.as_view(), name="staf"),
    path('add-user', CreateUser.as_view(), name="add-user"),
    path('<int:pk>', UserDetail.as_view(), name="user-details"),
    path('<int:pk>/edit', UserUpdateView.as_view(), name="user-update"),
    path('login/', login_view, name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
