from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Category, Product, Transaction, Expense, Consignment

def home(request):
    today = timezone.now().date()
    
    # 1. Weekly Calculations (Last 7 days)
    week_ago = today - timezone.timedelta(days=7)
    weekly_transactions = Transaction.objects.filter(date__gte=week_ago)
    weekly_expenses = Expense.objects.filter(date__gte=week_ago)
    weekly_consignments = Consignment.objects.filter(settlement_date__gte=week_ago, is_settled=True)
    
    weekly_revenue = sum(tx.total_price for tx in weekly_transactions) + sum(c.amount_received for c in weekly_consignments) or 0
    weekly_capital = sum(tx.quantity * tx.product.purchase_price for tx in weekly_transactions) + sum(c.quantity_sold * c.product.purchase_price for c in weekly_consignments) or 0
    weekly_expense = sum(exp.amount for exp in weekly_expenses) or 0
    weekly_profit = weekly_revenue - weekly_capital - weekly_expense

    # 2. Monthly Calculations (Current Month)
    monthly_transactions = Transaction.objects.filter(date__year=today.year, date__month=today.month)
    monthly_expenses = Expense.objects.filter(date__year=today.year, date__month=today.month)
    monthly_consignments = Consignment.objects.filter(settlement_date__year=today.year, settlement_date__month=today.month, is_settled=True)
    
    monthly_revenue = sum(tx.total_price for tx in monthly_transactions) + sum(c.amount_received for c in monthly_consignments) or 0
    monthly_capital = sum(tx.quantity * tx.product.purchase_price for tx in monthly_transactions) + sum(c.quantity_sold * c.product.purchase_price for c in monthly_consignments) or 0
    monthly_expense = sum(exp.amount for exp in monthly_expenses) or 0
    monthly_profit = monthly_revenue - monthly_capital - monthly_expense

    # 3. Yearly Calculations (Current Year)
    yearly_transactions = Transaction.objects.filter(date__year=today.year)
    yearly_expenses = Expense.objects.filter(date__year=today.year)
    yearly_consignments = Consignment.objects.filter(settlement_date__year=today.year, is_settled=True)
    
    yearly_revenue = sum(tx.total_price for tx in yearly_transactions) + sum(c.amount_received for c in yearly_consignments) or 0
    yearly_capital = sum(tx.quantity * tx.product.purchase_price for tx in yearly_transactions) + sum(c.quantity_sold * c.product.purchase_price for c in yearly_consignments) or 0
    yearly_expense = sum(exp.amount for exp in yearly_expenses) or 0
    yearly_profit = yearly_revenue - yearly_capital - yearly_expense

    # Fetch products for stock indicator
    products = Product.objects.all()

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

        'products': products,
    }

    return render(request, 'store/home.html', context)

def summary_bisnis(request):
    product_type = request.GET.get('type', 'pulsa')
    today = timezone.now().date()
    current_year = today.year

    if product_type == 'teri':
        title = "Ikan Teri"
        products_query = Product.objects.filter(name__icontains='teri')
        lifetime_consignments = Consignment.objects.filter(product__name__icontains='teri', is_settled=True)
        total_lifetime_capital = sum(c.quantity_sold * c.product.purchase_price for c in lifetime_consignments) or 0
        
        # Get all distinct years from settlements
        settlement_years = Consignment.objects.filter(product__name__icontains='teri', is_settled=True).dates('settlement_date', 'year')
        years_set = {d.year for d in settlement_years}
        years_set.add(current_year)
        
        yearly_summaries = []
        for yr in sorted(years_set, reverse=True):
            yr_consignments = Consignment.objects.filter(settlement_date__year=yr, is_settled=True, product__name__icontains='teri')
            yr_expenses = Expense.objects.filter(date__year=yr, product__name__icontains='teri')
            yr_rev = sum(c.amount_received for c in yr_consignments) or 0
            yr_cap = sum(c.quantity_sold * c.product.purchase_price for c in yr_consignments) or 0
            yr_exp = sum(exp.amount for exp in yr_expenses) or 0
            yearly_summaries.append({
                'year': yr,
                'revenue': yr_rev,
                'capital': yr_cap,
                'expense': yr_exp,
                'profit': yr_rev - yr_cap - yr_exp,
            })
    else:
        title = "Pulsa Telemor"
        products_query = Product.objects.filter(name__icontains='pulsa')
        lifetime_transactions = Transaction.objects.filter(product__name__icontains='pulsa')
        total_lifetime_capital = sum(tx.quantity * tx.product.purchase_price for tx in lifetime_transactions) or 0
        
        # Get all distinct years from transactions
        tx_years = Transaction.objects.filter(product__name__icontains='pulsa').dates('date', 'year')
        years_set = {d.year for d in tx_years}
        years_set.add(current_year)
        
        yearly_summaries = []
        for yr in sorted(years_set, reverse=True):
            yr_transactions = Transaction.objects.filter(date__year=yr, product__name__icontains='pulsa')
            yr_expenses = Expense.objects.filter(date__year=yr, product__name__icontains='pulsa')
            yr_rev = sum(tx.total_price for tx in yr_transactions) or 0
            yr_cap = sum(tx.quantity * tx.product.purchase_price for tx in yr_transactions) or 0
            yr_exp = sum(exp.amount for exp in yr_expenses) or 0
            yearly_summaries.append({
                'year': yr,
                'revenue': yr_rev,
                'capital': yr_cap,
                'expense': yr_exp,
                'profit': yr_rev - yr_cap - yr_exp,
            })

    # Current Stock Capital
    current_stock_capital = sum(p.stock * p.purchase_price for p in products_query) or 0

    # Monthly breakdown for current year (January to December)
    months_data = []
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    for m in range(1, 13):
        if product_type == 'teri':
            m_consignments = Consignment.objects.filter(settlement_date__year=current_year, settlement_date__month=m, is_settled=True, product__name__icontains='teri')
            m_expenses = Expense.objects.filter(date__year=current_year, date__month=m, product__name__icontains='teri')
            rev = sum(c.amount_received for c in m_consignments) or 0
            exp = sum(exp.amount for exp in m_expenses) or 0
        else:
            m_transactions = Transaction.objects.filter(date__year=current_year, date__month=m, product__name__icontains='pulsa')
            m_expenses = Expense.objects.filter(date__year=current_year, date__month=m, product__name__icontains='pulsa')
            rev = sum(tx.total_price for tx in m_transactions) or 0
            exp = sum(exp.amount for exp in m_expenses) or 0

        months_data.append({
            'month': month_names[m - 1],
            'revenue': rev,
            'expense': exp,
        })

    context = {
        'title': title,
        'current_stock_capital': current_stock_capital,
        'total_lifetime_capital': total_lifetime_capital,
        'months_data': months_data,
        'current_year': current_year,
        'yearly_summaries': yearly_summaries,
    }
    return render(request, 'store/summary_bisnis.html', context)

def category_list(request):
    action = request.POST.get('action')
    if request.method == 'POST':
        if action == 'create':
            name = request.POST.get('name')
            if name:
                Category.objects.create(name=name)
                return redirect('category_list')
        elif action == 'update':
            category_id = request.POST.get('category_id')
            name = request.POST.get('name')
            if category_id and name:
                cat = Category.objects.get(id=category_id)
                cat.name = name
                cat.save()
                return redirect('category_list')
        elif action == 'delete':
            category_id = request.POST.get('category_id')
            if category_id:
                Category.objects.filter(id=category_id).delete()
                return redirect('category_list')

    edit_id = request.GET.get('edit')
    edit_category = Category.objects.get(id=edit_id) if edit_id else None
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories, 'edit_category': edit_category})

def product_list(request):
    action = request.POST.get('action')
    if request.method == 'POST':
        if action == 'create':
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
        elif action == 'update':
            product_id = request.POST.get('product_id')
            name = request.POST.get('name')
            category_id = request.POST.get('category_id')
            purchase_price = request.POST.get('purchase_price')
            selling_price = request.POST.get('selling_price')
            stock = request.POST.get('stock')

            if product_id and name and category_id and purchase_price and selling_price:
                prod = Product.objects.get(id=product_id)
                prod.name = name
                prod.category = Category.objects.get(id=category_id)
                prod.purchase_price = purchase_price
                prod.selling_price = selling_price
                prod.stock = stock or 0
                prod.save()
                return redirect('product_list')
        elif action == 'delete':
            product_id = request.POST.get('product_id')
            if product_id:
                Product.objects.filter(id=product_id).delete()
                return redirect('product_list')

    edit_id = request.GET.get('edit')
    edit_product = Product.objects.get(id=edit_id) if edit_id else None
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {'products': products, 'categories': categories, 'edit_product': edit_product})

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
        product_id = request.POST.get('product_id')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if description and amount:
            product = Product.objects.get(id=product_id) if product_id else None
            Expense.objects.create(
                product=product,
                description=description,
                amount=amount
            )
            return redirect('expense_list')

    products = Product.objects.all()
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'store/expense_list.html', {'products': products, 'expenses': expenses})

def consignment_list(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'drop_off':
            product_id = request.POST.get('product_id')
            quantity_dropped = request.POST.get('quantity_dropped')
            if product_id and quantity_dropped:
                product = Product.objects.get(id=product_id)
                Consignment.objects.create(
                    product=product,
                    quantity_dropped=int(quantity_dropped)
                )
                return redirect('consignment_list')
                
        elif action == 'settle':
            consignment_id = request.POST.get('consignment_id')
            quantity_sold = request.POST.get('quantity_sold')
            amount_received = request.POST.get('amount_received')
            if consignment_id and quantity_sold and amount_received:
                item = Consignment.objects.get(id=consignment_id)
                item.quantity_sold = int(quantity_sold)
                item.amount_received = amount_received
                item.settlement_date = timezone.now().date()
                item.is_settled = True
                item.save()
                return redirect('consignment_list')

    products = Product.objects.all()
    consignments = Consignment.objects.all().order_by('-drop_off_date')
    return render(request, 'store/consignment_list.html', {'products': products, 'consignments': consignments})
