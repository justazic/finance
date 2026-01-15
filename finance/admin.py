from django.contrib import admin
from .models import Wallet,Income,Expense,IncomeCategory,ExpenceCategory

# Register your models here.


admin.site.register(Wallet)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(IncomeCategory)
admin.site.register(ExpenceCategory)
