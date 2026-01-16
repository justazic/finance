from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User



class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if user:
            return render(request, 'accounts/register.html', {'error': 'Bu username band!'})
        
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    
    
class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'accounts/login.html', {'error': 'Login yoki parol notogri'})
    
    
class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')