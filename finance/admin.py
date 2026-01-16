from django.contrib import admin
from .models import Wallet, Income, Expense, IncomeCategory, ExpenceCategory

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance', 'currency')
    list_filter = ('currency', 'user')

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'category', 'ammount', 'currency', 'created_at')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'category', 'ammount', 'currency', 'created_at')

admin.site.register(IncomeCategory)
admin.site.register(ExpenceCategory)