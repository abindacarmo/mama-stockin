from django.contrib import admin
from .models import Category, Product, Transaction, Expense, Consignment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Expense)
admin.site.register(Consignment)
