from django.shortcuts import render
from .models import Category

def home(request):
    return render(request, 'store/home.html')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

def product_list(request):
    return render(request, 'store/product_list.html')

def transaction_list(request):
    return render(request, 'store/transaction_list.html')

def expense_list(request):
    return render(request, 'store/expense_list.html')
