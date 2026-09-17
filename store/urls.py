from django.urls import path
from .views import home, category_list, product_list, transaction_list, expense_list, consignment_list, summary_bisnis

urlpatterns = [
    path('', home, name='store_home'),
    path('categories/', category_list, name='category_list'),
    path('products/', product_list, name='product_list'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('expenses/', expense_list, name='expense_list'),
    path('consignments/', consignment_list, name='consignment_list'),
    path('summary/', summary_bisnis, name='summary_bisnis'),
]
