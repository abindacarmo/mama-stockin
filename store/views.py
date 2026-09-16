from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Category, Product, Transaction, Expense

def home(request):
    today = timezone.now().date()
    
    # 1. Weekly Calculations (Last 7 days)
    week_ago = today - timezone.timedelta(days=7)
    weekly_transactions = Transaction.objects.filter(date__gte=week_ago)
    weekly_expenses = Expense.objects.filter(date__gte=week_ago)
    
    weekly_revenue = sum(tx.total_price for tx in weekly_transactions) or 0
    weekly_capital = sum(tx.quantity * tx.product.purchase_price for tx in weekly_transactions) or 0
    weekly_expense = sum(exp.amount for exp in weekly_expenses) or 0
    weekly_profit = weekly_revenue - weekly_capital - weekly_expense

    # 2. Monthly Calculations (Current Month)
    monthly_transactions = Transaction.objects.filter(date__year=today.year, date__month=today.month)
    monthly_expenses = Expense.objects.filter(date__year=today.year, date__month=today.month)
    
    monthly_revenue = sum(tx.total_price for tx in monthly_transactions) or 0
    monthly_capital = sum(tx.quantity * tx.product.purchase_price for tx in monthly_transactions) or 0
    monthly_expense = sum(exp.amount for exp in monthly_expenses) or 0
    monthly_profit = monthly_revenue - monthly_capital - monthly_expense

    # 3. Yearly Calculations (Current Year)
    yearly_transactions = Transaction.objects.filter(date__year=today.year)
    yearly_expenses = Expense.objects.filter(date__year=today.year)
    
    yearly_revenue = sum(tx.total_price for tx in yearly_transactions) or 0
    yearly_capital = sum(tx.quantity * tx.product.purchase_price for tx in yearly_transactions) or 0
    yearly_expense = sum(exp.amount for exp in yearly_expenses) or 0
    yearly_profit = yearly_revenue - yearly_capital - yearly_expense

    context = {
        'weekly_capital': weekly_capital,
        'weekly_revenue': weekly_revenue,
        'weekly_expense': weekly_expense,
        'weekly_profit': weekly_profit,
        
        'monthly_capital': monthly_capital,
        'monthly_revenue': monthly_revenue,
        'monthly_expense': monthly_expense,
        'monthly_profit': monthly_profit,
        
        'yearly_capital': yearly_capital,
        'yearly_revenue': yearly_revenue,
        'yearly_expense': yearly_expense,
        'yearly_profit': yearly_profit,
    }

    return render(request, 'store/home.html', context)

def category_list(request):
    if request.method == 'POST':
        name = request.POST.get('name_category')
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
