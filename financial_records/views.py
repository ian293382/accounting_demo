from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from .models import Groups,Category,FinancialRecord

from .form import FinancialRecordForm,CategoryForm

from django.http import HttpResponse
import csv


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

            record.group = group
            record.save()
            return redirect('groups:detail_group', group_pk)
    else:
        form = FinancialRecordForm()
        # Limit category choices to those belonging to the specified group
        form.fields['category'].queryset = Category.objects.filter(group=group, created_by=request.user)

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
        # Limit category to those belonging to the sqpcified group
        form.fields['category'].queryset = Category.objects.filter(group=group, created_by=request.user)
        

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


def export_csv(request, group_pk):
    group = get_object_or_404(Groups, id=group_pk)  
    records = FinancialRecord.objects.filter(group=group, created_by=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'category', 'description', 'debit', 'credit', 'currency', 'balance', 'created_at'])

    for record in records:

        categories = " ".join([category.name for category in record.category.all()])

        writer.writerow([
            record.name,
            categories,
            record.description,
            record.debit,
            record.credit,
            record.currency,
            record.balance,
            record.created_at,
        ])

    return response