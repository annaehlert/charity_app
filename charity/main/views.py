from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from main.models import Donation, Institution


class LandingPage(View):
    def get(self, request):
        donation = Donation.objects.values_list('quantity', flat=True)
        institution_number = Institution.objects.values_list('name', flat=True).count()
        institutions = Institution.objects.all()
        ctx = {
            "donation": sum(donation),
            "institution_number": institution_number,
            "institutions": institutions
        }
        return render(request, 'index.html', ctx)


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect('main')
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            request=request,
            username=request.POST.get('email'),
            password=request.POST.get('password')
        )
        if user is None:
            messages.add_message(request, messages.WARNING, 'Profil o podanych danych nie istnieje.')
            return redirect('login')
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Zostałeś poprawnie zalogowany.')
        return redirect('main')

class Register(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect('main')
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        password = request.POST.get('password')
        password_2 = request.POST.get('password2')
        if password != password_2:
            messages.add_message(request, messages.WARNING, 'Błędnie powtórzone hasło. Spróbuj jeszcze raz.')
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.WARNING, 'Profil o podanych danych już istnieje.')
            return render(request, 'register.html')
        User.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                 last_name=last_name)
        return redirect('login')