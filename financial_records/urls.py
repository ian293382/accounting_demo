from django.urls import path
from . import views

app_name = 'financial_records'

urlpatterns = [
    path('groups/<int:group_pk>/categories/create-category/', views.create_category, name='create_category'), 
    path('groups/<int:group_pk>/categories/<int:category_pk>/edit/', views.edit_category, name='edit_category'),
    path('groups/<int:group_pk>/categories/<int:category_pk>/delete/', views.delete_category, name='delete_category'),

    path('groups/<int:group_pk>/records/create-record/', views.create_record, name='create_record'),
    
]


#  path('<int:group_pk>/categories/<int:category_pk>/edit/', views.edit_category, name='edit_category'),