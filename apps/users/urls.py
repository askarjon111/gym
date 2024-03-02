from django.urls import path
from apps.users.views import (CreateUser, MembersListView, UserDetail,
                              UserRegistrationView, login_view, LogOutView,
                              UserUpdateView, StaffListView, is_user_registered,
                              register_new_user)


urlpatterns = [
    path('', MembersListView.as_view(), name="users"),
    path('staff/', StaffListView.as_view(), name="staff"),
    path('add-user', CreateUser.as_view(), name="add-user"),
    path('<int:pk>', UserDetail.as_view(), name="user-details"),
    path('<int:pk>/edit', UserUpdateView.as_view(), name="user-update"),
    path('login/', login_view, name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),

    # Telegram apis
    path('telegram/<int:tg_id>/', is_user_registered, name='user-registered'),
    path('telegram/register/', register_new_user, name='register-new-user'),
]
