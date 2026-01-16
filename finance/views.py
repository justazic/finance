from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, timedelta
from .models import Wallet, Income, Expense, IncomeCategory, ExpenceCategory, convert_curency
from decimal import Decimal
from django.contrib import messages
# Create your views here.


class DashboardView(View):
    def get(self, request):
        selected_date = date.today()
        selected_date_str = request.GET.get('date')
        if selected_date_str:
            try:
                selected_date = date.fromisoformat(selected_date_str)
            except Exception as e:
                selected_date = date.today()
        
        wallets = Wallet.objects.none()
        total_income = Decimal('0')
        total_expense = Decimal('0')
        total_balance_uzs = Decimal('0')

        if request.user.is_authenticated:
            wallets = Wallet.objects.filter(user=request.user)
            incomes = Income.objects.filter(user=request.user, created_at__date=selected_date)
            expenses = Expense.objects.filter(user=request.user, created_at__date=selected_date)
            total_income = sum(i.ammount for i in incomes)
            total_expense = sum(e.ammount for e in expenses)
            for w in wallets:
                total_balance_uzs +=convert_curency(w.balance,w.currency, 'UZS')
                
        total_balance_usd = convert_curency(total_balance_uzs, 'UZS', 'USD')
        total_balance_rub = convert_curency(total_balance_uzs, 'UZS', 'RUB')
        context = {'wallets': wallets,'total_income': total_income,'selected_date':selected_date,'total_expense': total_expense,'total_balance_uzs': round(total_balance_uzs, 2),'total_balance_usd':round(total_balance_usd, 2), 'total_balance_rub':round(total_balance_rub, 2)}

        return render(request, 'finance/dashboard.html', context)
    
    
class IncomeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        categories = IncomeCategory.objects.all()
        return render(
            request,
            'finance/income_form.html',
            {'wallet': wallets, 'categories': categories}
        )

    def post(self, request):
        try:
            wallet_id = request.POST.get('account')
            category_id = request.POST.get('category')
            currency = request.POST.get('currency')
            comment = request.POST.get('comment', '')
            ammount_raw = request.POST.get('ammount')
            if not ammount_raw:
                raise ValueError("Miqdor kiritilmadi")
            ammount = Decimal(ammount_raw)
            if ammount <= 0:
                raise ValueError("Miqdor 0 dan katta bolishi kerak")
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
            Income.objects.create(user=request.user,wallet=wallet,category_id=category_id,ammount=ammount,currency=currency,comment=comment)
            messages.success(request, "Kirim muvaffaqiyatli qoshildi")
            return redirect('dashboard')
        except Wallet.DoesNotExist:
            messages.error(request, "Hisob topilmadi")
        except Exception as e:
            messages.error(request, str(e))
        return redirect('income_add')

    
    
class ExpenseCreateView(LoginRequiredMixin, View):
    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        categories = ExpenceCategory.objects.all()
        return render(
            request,
            'finance/expense_form.html',
            {'wallet': wallets, 'categories': categories}
        )

    def post(self, request):
        try:
            wallet_id = request.POST.get('account')
            category_id = request.POST.get('category')
            currency = request.POST.get('currency')
            comment = request.POST.get('comment', '').strip()
            ammount_raw = request.POST.get('ammount')
            if not ammount_raw:
                raise ValueError("Miqdor kiritilmadi")
            ammount = Decimal(ammount_raw)
            if ammount <= 0:
                raise ValueError("Miqdor 0 dan katta bolishi kerak")
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
            Expense.objects.create(user=request.user,wallet=wallet,category_id=category_id,ammount=ammount,currency=currency,comment=comment)
            messages.success(request, "Chiqim muvaffaqiyatli qoshildi")
            return redirect('dashboard')
        except Wallet.DoesNotExist:
            messages.error(request, "Hisob topilmadi")
        except Exception as e:
            messages.error(request, str(e))
        return redirect('expense_add')
    
    
class WalletCreateView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'finance/wallet_form.html')
    
    def post(self, request):
        Wallet.objects.create(user=request.user, name=request.POST.get('name'), balance=request.POST.get('balance'), currency=request.POST.get('currency'))
        return redirect('dashboard')
    
    
class DailyReportView(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()
        incomes = Income.objects.filter(user=request.user, created_at__date=today)
        expenses = Expense.objects.filter(user=request.user, created_at__date=today)
        total_income = sum(i.ammount for i in incomes)
        total_expense = sum(e.ammount for e in expenses)
        
        return render(request, 'finance/report_daily.html', {'incomes':incomes, 'expenses':expenses,'total_income':total_income,'total_expense':total_expense})
    
    
class WeeklyReportView(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
        incomes = Income.objects.filter(user=request.user, created_at__gte=start_date)
        expenses = Expense.objects.filter(user=request.user, created_at__gte= start_date)
        total_income = sum(i.ammount for i in incomes)
        total_expense = sum(e.ammount for e in expenses)
        return render(request, 'finance/report_weekly.html', {'incomes':incomes, 'expenses':expenses,'total_income':total_income,'total_expense':total_expense})
        
        
class MonthlyReportView(LoginRequiredMixin,View):
    def get(self,request):
        month = request.GET.get('month',date.today().month)
        year = date.today().year
        incomes = Income.objects.filter(user=request.user, created_at__month=month, created_at__year= year)
        expenses = Expense.objects.filter(user=request.user,created_at__month=month ,created_at__year= year)
        total_income = sum(i.ammount for i in incomes)
        total_expense = sum(e.ammount for e in expenses)
        return render(request, 'finance/report_monthly.html', {'incomes':incomes, 'expenses':expenses,'total_income':total_income,'total_expense':total_expense})
        