from django.shortcuts import render, redirect
from .models import Category, Product

def home(request):
    return render(request, 'store/home.html')

def category_list(request):
    if request.method == 'POST':
        name = request.POST.get('name_category') # foti husi attribute name="name_category" iha tag <input> nia laran(no nia fundsaun atu foti value ne'ebe prense husi user)
        if name:
            Category.objects.create(name=name) #name kor matak ne koluna husi tabela Category(nia funsaun atu halo lina foun iha tabela category)
            return redirect('category_list')

    categories = Category.objects.all() #foti dados sira iha database hodi fo sai fali iha template
    return render(request, 'store/category_list.html', {'categories': categories}) # template labele haree variable python(ne mak key) tamba ne utiliza contex dictionary

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
    products = Product.objects.all()
    return render(request, 'store/transaction_list.html', {'products': products})

def expense_list(request):
    return render(request, 'store/expense_list.html')
