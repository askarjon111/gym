from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from apps.users.models import Lead, User
from apps.users.forms import LeadForm
from apps.users.permissions import gym_manager_required
from project.settings import ERROR_PATTERN


@gym_manager_required(login_url='login')
def leads_view(request):
    leads = Lead.objects.filter(operator=request.user)

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.instance.operator = request.user
            form.save()
            return redirect('leads')
        else:
            errors = ERROR_PATTERN.search(str(form.errors)).group(1)
            messages.add_message(
                request, messages.WARNING, f"Ошибка: {errors}")
            return redirect('leads')
    else:
        query = request.GET.get('q', None)
        if query:
            leads = leads.filter(Q(first_name__contains=query) | Q(last_name__contains=query) | Q(phone_number__contains=query))
        paginator = Paginator(leads, 20)
        page = request.GET.get('page')

        try:
            leads = paginator.page(page)
        except PageNotAnInteger:
            leads = paginator.page(1)
        except EmptyPage:
            leads = paginator.page(paginator.num_pages)
        form = LeadForm()
    return render(request, 'users/leads.html', {'form': form, 'objects': leads})


@gym_manager_required(login_url='login')
def lead_edit_view(request, pk):
    lead = Lead.objects.get(pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
    else:
        form = LeadForm(instance=lead)
    return render(request, 'users/lead_edit.html', {'form': form, 'lead': lead})


@gym_manager_required(login_url='login')
def lead_delete_view(request, pk):
    lead = Lead.objects.get(pk=pk)
    if request.method == 'POST':
        lead.delete()
        return redirect('leads')
    return render(request, 'lead_delete.html', {'lead': lead})


def activate_lead_view(request):
    if request.method == 'POST':
        lead = Lead.objects.filter(id=request.POST.get('member')).first()
        user, _ = User.objects.update_or_create(phone_number=lead.phone_number,
                                                defaults={'first_name': lead.first_name, 'last_name': lead.last_name})
        user.gyms.add(request.user.gym)
        user.save()
        lead.status = Lead.STATUS_CHOICES[2][0]
        lead.save()
        return redirect('user-details', pk=user.pk)


@gym_manager_required(login_url='login')
def cancel_lead_view(request):
    if request.method == 'POST':
        lead = Lead.objects.filter(id=request.POST.get('member')).first()
        lead.status = Lead.STATUS_CHOICES[3][0]
        lead.save()
        return redirect('leads')


__all__ = ['leads_view', 'lead_edit_view', 'lead_delete_view', 'activate_lead_view', 'cancel_lead_view']
