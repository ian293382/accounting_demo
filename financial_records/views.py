from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from .models import Groups

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