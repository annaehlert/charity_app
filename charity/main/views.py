from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from main.forms import LoginForm, RegistrationForm
from main.models import Donation, Institution


class LandingPage(View):
    def get(self, request):
        # zliczenie ilości oddanych worków, suma wyciągnięta z bazy danych, aggregate(Sum()) zwraca słownik
        donation = Donation.objects.aggregate(Sum('quantity'))
        #zliczenie ilości fundacji, którym została udzielona pomoc
        institution_number = Institution.objects.all().count()
        institutions = Institution.objects.all()
        user = request.user
        ctx = {
            "donation": donation.get('quantity__sum'),
            "institution_number": institution_number,
            "institutions": institutions,
            "user": user
        }
        return render(request, 'index.html', ctx)


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect('main')
        return render(request, 'login.html',
        {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "login.html",
                {"form": form}
            )
        user = authenticate(
            request=request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is None:
            # messages.add_message(request, messages.WARNING, 'Profil o podanych danych nie istnieje.')
            return redirect('login')
        login(request, user)
        # messages.add_message(request, messages.SUCCESS, 'Zostałeś poprawnie zalogowany.')
        return redirect('main')


class Register(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect('main')

        return render(request, 'register.html',
                      {"form": RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'register.html',
                          {"form": form})
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['name']
        last_name = form.cleaned_data['surname']
        password = form.cleaned_data['password']
        password_2 = form.cleaned_data['password2']
        if password != password_2:
            messages.add_message(request, messages.WARNING, 'Błędnie powtórzone hasło. Spróbuj jeszcze raz.')
            return render(request, 'register.html',
                          {"form": form})
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.WARNING, 'Profil o podanym emailu już istnieje.')
            return render(request, 'register.html',
                          {"form": form})
        User.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                 last_name=last_name)
        return redirect('login')


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')