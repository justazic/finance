from django.urls import path
from .views import DashboardView,IncomeCreateView,ExpenseCreateView,DailyReportView,WeeklyReportView,MonthlyReportView,WalletCreateView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('income/add/', IncomeCreateView.as_view(), name='income_add'),
    path('expense/add/', ExpenseCreateView.as_view(), name='expense_add'),
    path('wallet/add/', WalletCreateView.as_view(), name='wallet_add'),
    path('report/daily/', DailyReportView.as_view(), name='daily_report'),
    path('report/weekly/', WeeklyReportView.as_view(), name='weekly_report'),
    path('report/monthly/', MonthlyReportView.as_view(), name='monthly_report'),
    
]