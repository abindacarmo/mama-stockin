from django.shortcuts import render, redirect
from .models import Category, Product, Transaction, Expense

def home(request):
    return render(request, 'store/home.html')

def category_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('category_list')

    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

def product_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        purchase_price = request.POST.get('purchase_price')
        selling_price = request.POST.get('selling_price')
        stock = request.POST.get('stock')

        if name and category_id and purchase_price and selling_price:
            category = Category.objects.get(id=category_id)
            Product.objects.create(
                name=name,
                category=category,
                purchase_price=purchase_price,
                selling_price=selling_price,
                stock=stock or 0
            )
            return redirect('product_list')

    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {'products': products, 'categories': categories})

def transaction_list(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        if product_id and quantity:
            product = Product.objects.get(id=product_id)
            Transaction.objects.create(
                product=product,
                quantity=int(quantity)
            )
            return redirect('transaction_list')

    products = Product.objects.all()
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'store/transaction_list.html', {'products': products, 'transactions': transactions})

def expense_list(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if description and amount:
            Expense.objects.create(
                description=description,
                amount=amount
            )
            return redirect('expense_list')

    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'store/expense_list.html', {'expenses': expenses})
