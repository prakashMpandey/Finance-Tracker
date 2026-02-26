from django.contrib import admin
from django.urls import path
from .views import create_transaction,get_transactions,dashboard_data,delete_transaction,edit_transaction,get_analytics

urlpatterns = [
path("dashboard/",dashboard_data,name="dashboard"),
path('create/',create_transaction,name="create_transaction"),
path('transactions/',get_transactions,name="transactions"),
path('<int:t_id>/delete/',delete_transaction,name="delete_transaction"),
path('<int:t_id>/edit/',edit_transaction,name="edit_transaction"),
path('analytics/',get_analytics,name='analytics')
]
