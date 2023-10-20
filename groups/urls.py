from django.urls import path

from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.groups, name='groups'),
    path('<int:pk>/', views.detail_group, name='detail_group'),
    path('<int:pk>/edit/', views.edit_group, name='edit_group'),
    path('<int:pk>/delete/', views.delete_group, name='delete_group'),
    path('create-group/', views.create_group, name='create_group'),
    
] 