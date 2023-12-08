from django.urls import path
from apps.users.views import CreateUser, MarkAttendanceView, MembersListView, UserDetail, login_view, LogOutView


urlpatterns = [
    path('', MembersListView.as_view(), name="users"),
    path('add-user', CreateUser.as_view(), name="add-user"),
    path('<int:pk>', UserDetail.as_view(), name="user-details"),
    path('mark-attendance/', MarkAttendanceView.as_view(), name='mark-attendance'),
    path('login/', login_view, name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
]

