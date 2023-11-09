from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from .models import Groups,Category,FinancialRecord

from .form import FinancialRecordForm,CategoryForm,  CSVUploadForm

from django.http import HttpResponse
import csv
from django.utils import timezone

from datetime import datetime



@login_required
def create_category(request, group_pk):
    group = get_object_or_404(Groups, pk=group_pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.group = group  
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

            selected_categories = form.cleaned_data['category']       
          # 将用户选择的类别分配给记录
            record.category.set(selected_categories)

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

    # set from_date to_date
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

    if from_date_str and to_date_str:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
    else:
        # 預設
        from_date = datetime.now().replace(day=1)
        to_date = datetime.max

    records = FinancialRecord.objects.filter(
        group=group,
        created_by=request.user,
        created_at__range=(from_date, to_date)
    )

    # group_name = group.group_name 无法使用会导致跳转页面
    group_id = group.id
    current_time = timezone.now()
    time_str = current_time.strftime("%Y%m%d")
    file_name = f"{time_str}-from-group:{group_id}.csv"

  
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

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


from django.utils import timezone
from decimal import Decimal

def import_csv(request, group_pk):
    group = get_object_or_404(Groups, pk=group_pk)
   
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['data_file']
            decoded_data = csv_file.read().decode('utf-8').splitlines()
            csv_data = csv.reader(decoded_data)
            # 跳過第一段資料寫法

            # for _ in range(50):
            #      next(csv_data, None)
            next(csv_data, None) 

            for row in csv_data:
                category_name = row[1]
                category, created = Category.objects.get_or_create(name=category_name, group=group, created_by=request.user)

                
                financial_record = FinancialRecord(
                    group=group,
                    name=row[0],
                    description=row[2],
                    debit = Decimal(row[3]),
                    credit= Decimal(row[4]),
                    currency= Decimal(row[5]),
                    created_at=timezone.now(),
                    created_by= request.user
                    
                )
                financial_record.save()

                # conntect relationship Category = FinancialRecord
                financial_record.category.set([category])

            return redirect('groups:detail_group', group_pk)

    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})

from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime, timedelta
from calendar import monthrange

def analysis(request, group_pk):
    # string
    group = get_object_or_404(Groups, pk=group_pk)
    
    from_date = request.GET.get('from_date') 
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
    else:
        # 使用預設日期範圍
        current_month = timezone.now().month
        current_year = timezone.now().year
        

        if current_month == 12:
            to_date = datetime(current_year + 1, 1, 1) - timedelta(days=1)
        else:
            to_date = datetime(current_year, current_month + 1, 1) - timedelta(days=1)
            from_date = datetime(current_year, current_month, 1)
    # 計算日期範圍內的每日 debit 總和
    data_dict = {}
    while from_date <= to_date:
        daily_expenses = FinancialRecord.objects.filter(
            group=group,
            created_at__date=from_date,
            currency=1.0,
        ).aggregate(Sum('debit'))['debit__sum'] or 0
        data_dict[from_date.strftime('%Y-%m-%d')] = daily_expenses
        from_date += timedelta(days=1)

    # 將日期和總和轉換為列表
    labels = list(data_dict.keys())
    total_debits = list(data_dict.values())

    data = {
        "labels": labels,
        "total_debits": total_debits,
    }

    return JsonResponse(data)