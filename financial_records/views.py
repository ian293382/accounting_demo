from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from .models import Groups,Category,FinancialRecord

from .form import FinancialRecordForm,CategoryForm

@login_required
def create_category(request, group_pk):
    group = get_object_or_404(Groups, pk=group_pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.group = group  # 设置关联的群组
            category.created_by = request.user
       
            category.save()

            return redirect('groups:detail_group', group_pk)

    else:
        form = CategoryForm()

    return render(request, 'financial_records/create_category.html', {
        'form': form,
        'group': group,
    })

@login_required
def edit_category(request, group_pk, category_pk):
    group = get_object_or_404(Groups, id=group_pk)
    category = get_object_or_404(Category, group=group, pk=category_pk, created_by=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()

            return redirect('groups:detail_group', group_pk)

    else:
        form = CategoryForm(instance=category)
        form.fields['name'].queryset = Category.objects.filter(created_by=request.user, group=group)

    return render(request, 'financial_records/create_category.html',{
        'form': form,
        'title': 'Edit Category',
        
    })

@login_required
def delete_category(request, group_pk, category_pk):
    group = get_object_or_404(Groups, id=group_pk)
    category = get_object_or_404(Category, group=group, pk=category_pk, created_by=request.user)

    category.delete()

    return redirect('groups:detail_group', group_pk)


@login_required
def create_record(request, group_pk):
    group = get_object_or_404(Groups, pk=group_pk)

    if request.method == 'POST':
        form = FinancialRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            # record.category = category.name
            record.group = group
            record.save()

            return redirect('groups:detail_group', group_pk)
    else:
        form = FinancialRecordForm()
        form.fields['category'].queryset = Category.objects.filter(created_by=request.user)

    return render(request, 'financial_records/create_record.html', {
        'form': form,
        'group': group,
    })

@login_required
def edit_record(request, group_pk, record_pk):
    group = get_object_or_404(Groups, id=group_pk, created_by=request.user)
    record = get_object_or_404(FinancialRecord, group=group, pk=record_pk, created_by=request.user)

    if request.method == 'POST':
        form = FinancialRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()

            return redirect('groups:detail_group', group_pk)

    else:
        form = FinancialRecordForm(instance=record)
        

    return render(request, 'financial_records/create_category.html',{
        'form': form,
        'title': 'Edit Category',
        
    })

@login_required
def delete_record(request, group_pk, record_pk):
    group = get_object_or_404(Groups, id=group_pk)
    record = get_object_or_404(FinancialRecord, group=group, pk=record_pk, created_by=request.user)

    record.delete()

    return redirect('groups:detail_group', group_pk)

