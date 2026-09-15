from django.contrib import admin
from .models import Category, Product, Transaction, Expense

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Expense)
