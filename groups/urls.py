from django.urls import path

from . import views 

from financial_records.views import create_category  # 这里是导入financial_records/views.py中的视图

app_name = 'groups'

urlpatterns = [
    path('', views.groups, name='groups'),
    path('<int:pk>/', views.detail_group, name='detail_group'),
    path('<int:pk>/edit/', views.edit_group, name='edit_group'),
    path('<int:pk>/delete/', views.delete_group, name='delete_group'),
    path('create-group/', views.create_group, name='create_group'),
    path('<int:group_pk>/create-category/', create_category, name='create_category'),
    
] 