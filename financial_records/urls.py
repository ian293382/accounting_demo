from django.urls import path
from . import views

app_name = 'financial_records'

urlpatterns = [
     path('<int:group_pk>/categories/create-category/', views.create_category, name='create_category'), 
  
]