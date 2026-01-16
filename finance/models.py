from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
def convert_curency(ammount,from_curency, to_curency):
    ammount = Decimal(str(ammount))
    rates ={'UZS':1, 'USD':12500,'RUB': 135}
    ammount_in_uzs = ammount * rates[from_curency]
    return ammount_in_uzs / rates[to_curency]

class Wallet(models.Model):
    CURRENCY_CHOICES = (("UZS", "Som"),("USD", "Dollar"),("RUB", "Ruble"),)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    
    def __str__(self):
        return self.name 
    
    
class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class ExpenceCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True)
    ammount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Wallet.CURRENCY_CHOICES, default='UZS')
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        converted = convert_curency(self.ammount,self.currency,self.wallet.currency)
        self.wallet.balance += converted
        self.wallet.save()
        super().save(*args, **kwargs)
        
        
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenceCategory, on_delete=models.SET_NULL, null=True)
    ammount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Wallet.CURRENCY_CHOICES, default='UZS')
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        converted = convert_curency(self.ammount,self.currency,self.wallet.currency)
        self.wallet.balance -= converted
        self.wallet.save()
        super().save(*args, **kwargs)
        