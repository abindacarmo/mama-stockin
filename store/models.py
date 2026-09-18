from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # Automatically calculate total price: quantity * product selling price
        self.total_price = self.quantity * self.product.selling_price
        
        # Automatically reduce product stock
        if self.pk is None:  # Only reduce stock on creation
            self.product.stock -= self.quantity
            self.product.save()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale: {self.quantity}x {self.product.name} on {self.date}"

class Expense(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        prod_name = self.product.name if self.product else "General"
        return f"[{prod_name}] {self.description} - ${self.amount} ({self.date})"

class Consignment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_dropped = models.IntegerField()
    drop_off_date = models.DateField(auto_now_add=True)
    quantity_sold = models.IntegerField(default=0)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    settlement_date = models.DateField(null=True, blank=True)
    is_settled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # When a new consignment batch is dropped off, reduce product stock
        if self.pk is None:
            self.product.stock -= self.quantity_dropped
            self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Settled" if self.is_settled else "Active"
        return f"Consignment: {self.product.name} ({self.quantity_dropped} pcs) - {status}"
