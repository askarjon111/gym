from django.urls import path
from apps.users.viewss.access.views import AccessByUserView
from apps.users.viewss import (CreateUserView, UserRegistrationView, login_view,
                               LogOutView, StaffListView, MembersListView,
                               UserDetail, UserUpdateView, UserDelete,
                               register_user_view, is_registered_view)
from apps.users.viewss.user_profile import UserProfileUpdateView
from apps.users.viewss.lead import (activate_lead_view, lead_delete_view, leads_view,
                                    lead_edit_view, leads_view, cancel_lead_view)
from apps.users.viewss.sessions import my_sessions_view
from apps.users.viewss.subscription import my_subscription_view


urlpatterns = [
    path('', MembersListView.as_view(), name="users"),
    path('staff/', StaffListView.as_view(), name="staff"),
    path('add-user', CreateUserView.as_view(), name="add-user"),
    path('<int:pk>', UserDetail.as_view(), name="user-details"),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name="user-update"),
    path('<int:pk>/edit-profile/', UserProfileUpdateView.as_view(), name="user-profile-update"),
    path('<int:pk>/delete', UserDelete.as_view(), name="user-delete"),
    path('login/', login_view, name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),

    # Telegram apis
    path('telegram/is-registered/<int:tg_id>/', is_registered_view, name='user-registered'),
    path('telegram/register/', register_user_view, name='register-new-user'),
    path('telegram/my-subscription/<int:tg_id>/', my_subscription_view, name='my-subscription'),
    path('telegram/my-sessions/<int:tg_id>/', my_sessions_view, name='my-sessions'),

    # Leads:
    path('leads/', leads_view, name='leads'),
    path('leads/<int:pk>/', lead_edit_view, name='lead-edit'),
    path('leads/activate/',activate_lead_view,name='activate-lead'),
    path('leads/canceled/', cancel_lead_view,name='canceled_lead'),
    path('leads/<int:pk>/delete/', lead_delete_view, name='lead_delete'),

    # Access
    path('access/<int:user_id>/', AccessByUserView.as_view(), name='access-by-user'),
]
