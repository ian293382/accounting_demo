from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


from .form import GroupForm

from .models import Groups

from financial_records.models import Category,FinancialRecord

@login_required
def groups(request):
    # groups = Groups.objects.all()
    groups = Groups.objects.filter(created_by=request.user)

      
    return render(request, 'groups/groups.html', {
        'groups': groups,
    })

@login_required
def detail_group(request,pk):
    group = get_object_or_404(Groups, pk=pk, created_by=request.user)
    groups = Groups.objects.filter(created_by=request.user).exclude(pk=pk)

    categories = Category.objects.filter(created_by=request.user, group=group)

    return render(request, 'groups/detail_group.html', {
        'groups':groups,
        'group': group,
        'title': group.group_name,
        'categories': categories,
    })



@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user

            group.save()

            return redirect('/groups/')
        
    else:
        form = GroupForm()

    return render(request, 'groups/create_group.html',{
        'form': form,
        'title': 'Create financial Group',     
        })

@login_required
def edit_group(request, pk):
    group = get_object_or_404(Groups, created_by=request.user, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)

        if form.is_valid():
            form.save()

            return redirect('/groups/')
    else:
        form = GroupForm(instance=group)


    return render(request, 'groups/create_group.html',{
        'form': form,
        'title': 'Edit group',
    })            


@login_required
def delete_group(request, pk):
    group = get_object_or_404(Groups, created_by=request.user, pk=pk)

    group.delete()

    return redirect('/groups/')