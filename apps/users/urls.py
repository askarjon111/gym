from django.urls import path
from apps.users.views import (CreateUser, MembersListView, UserDetail, UserProfileUpdateView,
                              UserRegistrationView, activate_lead, canceled_lead, lead_delete, lead_edit, leads, login_view, LogOutView,
                              UserUpdateView, StaffListView, UserDelete,
                              is_user_registered, register_new_user, my_subscription, 
                              my_sessions)
from apps.users.viewss.access.views import AccessByUserView


urlpatterns = [
    path('', MembersListView.as_view(), name="users"),
    path('staff/', StaffListView.as_view(), name="staff"),
    path('add-user', CreateUser.as_view(), name="add-user"),
    path('<int:pk>', UserDetail.as_view(), name="user-details"),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name="user-update"),
    path('<int:pk>/edit-profile/', UserProfileUpdateView.as_view(), name="user-profile-update"),
    path('<int:pk>/delete', UserDelete.as_view(), name="user-delete"),
    path('login/', login_view, name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),

    # Telegram apis
    path('telegram/is-registered/<int:tg_id>/', is_user_registered, name='user-registered'),
    path('telegram/register/', register_new_user, name='register-new-user'),
    path('telegram/my-subscription/<int:tg_id>/', my_subscription, name='my-subscription'),
    path('telegram/my-sessions/<int:tg_id>/', my_sessions, name='my-sessions'),

    # Leads:
    path('leads/', leads, name='leads'),
    path('leads/<int:pk>/', lead_edit, name='lead-edit'),
    path('leads/activate/',activate_lead,name='activate-lead'),
    path('leads/canceled/',canceled_lead,name='canceled_lead'),
    path('leads/<int:pk>/delete/', lead_delete, name='lead_delete'),

    # Access
    path('access/<int:user_id>/', AccessByUserView.as_view(), name='access-by-user'),
]
