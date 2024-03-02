from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.websites.models import GymWebsite


def my_view(request):
    subdomain = request.subdomain
    site = GymWebsite.objects.filter(subdomain=subdomain).first()
    if site:
        return render(request, 'websites/design_1/index.html',
                    {'site': site})
    else:
        return redirect('dashboard')
