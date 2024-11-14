from django.urls import path
from .views import (AssignSalesRepsToSalesEngineers, EditSalesEngineerView, SalesEngineerView, NewSalesEngineerView,
                    NewSalesEngineerManagerView, check_username, check_email, SalesEngineerManagerView)

urlpatterns = [
    path('managers/sales_engineers', SalesEngineerView.as_view(), name='sales_engineers'),
    path('managers/se_managers', SalesEngineerManagerView.as_view() , name="se_managers"),
    path('managers/se_managers/new', NewSalesEngineerManagerView.as_view() , name="new_se_manager"),
    path("managers/sales_engineers/new", NewSalesEngineerView.as_view(), name='new_sales_engineer'),
    path('managers/sales_engineers/edit/<str:id>', EditSalesEngineerView.as_view(), name='sales_engineers_edit'),
    path('managers/sales_engineers/edit/<str:id>/sales_reps', AssignSalesRepsToSalesEngineers.as_view(), name='assign_sales_reps'),
    path("managers/sales_engineers/check-email", check_email, name='check_email'),
    path("managers/sales_engineers/check-username", check_username, name='check_username'),



]
