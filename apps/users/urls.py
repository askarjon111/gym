from django.urls import path
from apps.users.views import CreateUser, MembersListView, UserDetail, login_view, LogOutView, UserUpdateView


urlpatterns = [
    path('', MembersListView.as_view(), name="users"),
    path('add-user', CreateUser.as_view(), name="add-user"),
    path('<int:pk>', UserDetail.as_view(), name="user-details"),
    path('<int:pk>/edit', UserUpdateView.as_view(), name="user-update"),
    path('login/', login_view, name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
]

