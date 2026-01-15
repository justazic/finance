from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, timedelta
from .models import Wallet, Income, Expense, IncomeCategory, ExpenceCategory, convert_curency
from decimal import Decimal
# Create your views here.


class DashboardView(View):
    def get(self, request):
        wallets = Wallet.objects.none()
        incomes = Income.objects.none()
        expenses = Expense.objects.none()
        total_income = 0
        total_expense = 0
        total_balance = 0
        if request.user.is_authenticated:
            wallets = Wallet.objects.filter(user=request.user)
            incomes = Income.objects.filter(user=request.user)
            expense = Expense.objects.filter(user=request.user)
            total_income = sum(i.ammount for i in incomes)
            total_expense = sum(e.ammount for e in expense)
            
            for i in wallets:
                total_balance += convert_curency(i.balance,i.currency, 'UZS')
            
        return render(request, 'finance/dashboard.html', {'wallet': wallets,'total_income': total_income,'total_expense': total_expense,'total_balance':total_balance})
    
    
class IncomeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        wallet = Wallet.objects.filter(user=request.user)
        categories = IncomeCategory.objects.all()
        return render(request, 'finance/income_form.html', {'wallet': wallet, 'categories': categories})
    
    def post(self,request):
        wallet_id = request.POST.get('account')
        category_id = request.POST.get('category')
        ammount_raw = request.POST.get('ammount')
        currency=request.POST.get('currency')
        ammount = Decimal(ammount_raw)
        Income.objects.create(user=request.user,wallet_id=wallet_id,category_id=category_id, ammount=ammount,currency=currency)
        return redirect('dashboard')
    
    
class ExpenseCreateView(LoginRequiredMixin,View):
    def get(self, request):
        wallet = Wallet.objects.filter(user=request.user)
        categories = ExpenceCategory.objects.all()
        return render(request, 'finance/expense_form.html', {'wallet': wallet, 'categories': categories})
        
    def post(self,request):
        wallet_id = request.POST.get('account')
        category_id = request.POST.get('category')
        ammount_raw = request.POST.get('ammount')
        currency=request.POST.get('currency')
        ammount = Decimal(ammount_raw)
        Expense.objects.create(user=request.user,wallet_id=wallet_id,category_id=category_id, ammount=ammount, currency=currency)
        return redirect('dashboard')
    
    
class WalletCreateView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'finance/wallet_form.html')
    
    def post(self, request):
        Wallet.objects.create(user=request.user, name=request.POST.get('name'),card_number = request.POST.get('card_number') , balance=request.POST.get('balance'), currency=request.POST.get('currency'))
        return redirect('dashboard')
    
    
class DailyReportView(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()
        incomes = Income.objects.filter(user=request.user, created_at=today)
        expenses = Expense.objects.filter(user=request.user, created_at=today)
        
        return render(request, 'finance/report_daily.html', {'incomes':incomes, 'expenses':expenses})
    
    
class WeeklyReportView(LoginRequiredMixin, View):
    def get(self, request):
        start_date = date.today() - timedelta(days=7)
        incomes = Income.objects.filter(user=request.user, created_at__gte=start_date)
        expenses = Expense.objects.filter(user=request.user, created_at__gte= start_date)
        return render(request, 'finance/report_weekly.html', {'incomes':incomes, 'expenses':expenses})
        
        
class MonthlyReportView(LoginRequiredMixin,View):
    def get(self,request):
        month = date.today().month
        year = date.today().year
        incomes = Income.objects.filter(user=request.user, created_at__month=month, created_at__year= year)
        expenses = Expense.objects.filter(user=request.user,created_at__month=month ,created_at__year= year)
        return render(request, 'finance/report_monthly.html', {'incomes':incomes, 'expenses':expenses})
        