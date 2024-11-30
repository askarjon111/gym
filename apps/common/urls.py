from django.urls import path
from apps.common.views import home


urlpatterns = [
    path('', home, name='dashboard'),
]

