from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from main.forms import LoginForm, RegistrationForm, DonationForm
from main.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        # zliczenie ilości oddanych worków, suma wyciągnięta z bazy danych, aggregate(Sum()) zwraca słownik
        donation = Donation.objects.aggregate(Sum('quantity'))
        # zliczenie ilości fundacji, którym została udzielona pomoc
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


class AddDonation(View, LoginRequiredMixin):
    def get(self, request):
        categories = Category.objects.all()
        foundations = Institution.objects.all()
        form = DonationForm()
        ctx = {
            "categories": categories,
            "foundations": foundations,
            "form": form
        }
        return render(request, 'form.html', ctx)

    def post(self, request):
        # form = DonationForm(request.POST)
        # user = request.user
        # if not form.is_valid():
        #     categories = Category.objects.all()
        #     foundations = Institution.objects.all()
        #     form = DonationForm()
        #     ctx = {
        #         "categories": categories,
        #         "foundations": foundations,
        #         "form": form
        #     }
        #     return render(request, 'form.html', ctx)
        # categories = request.POST['categories']
        # quantity = request.POST['quantity']
        # institution = request.POST['institution']
        # address = request.POST['address']
        # city = request.POST['city']
        # zip_code = request.POST['zip_code']
        # phone_number = request.POST['phone_number']
        # pick_up_date = request.POST['pick_up_date']
        # pick_up_time = request.POST['pick_up_time']
        # pick_up_comment = request.POST['pick_up_comment']
        # new_donation = Donation.objects.create(
        #     quantity=quantity,
        #     institution=Institution.objects.get(id=int(institution)),
        #     address=address,
        #     phone_number=phone_number,
        #     city=city,
        #     zip_code=zip_code,
        #     pick_up_date=pick_up_date,
        #     pick_up_time=pick_up_time,
        #     pick_up_comment=pick_up_comment,
        #     user=User.objects.get(id=user.id)
        # )
        # for category in categories:
        #     new_category = Category.objects.get(id=category)
        #     new_donation.categories.add(new_category)
        # new_donation.save()
        # return render(request, 'form-confirmation.html')

        if request.is_ajax():
            form = DonationForm(request.POST)
            user = request.user
            if form.is_valid():
                categories = form.cleaned_data['categories']
                quantity = form.cleaned_data['bags']
                institution = form.cleaned_data['institution']
                address = form.cleaned_data['address']
                city = form.cleaned_data['city']
                zip_code = form.cleaned_data['zip_code']
                phone_number = form.cleaned_data['phone_number']
                pick_up_date = form.cleaned_data['pick_up_date']
                pick_up_time = form.cleaned_data['pick_up_time']
                pick_up_comment = form.cleaned_data['pick_up_comment']
                new_donation = Donation.objects.create(
                    quantity=quantity,
                    institution=institution,
                    address=address,
                    phone_number=phone_number,
                    city=city,
                    zip_code=zip_code,
                    pick_up_date=pick_up_date,
                    pick_up_time=pick_up_time,
                    pick_up_comment=pick_up_comment,
                    user=user
                )
                for category in categories:
                    # new_category = Category.objects.get(pk=category)
                    new_donation.categories.add(category)
                new_donation.save()
                # return render(request, 'form-confirmation.html')
                return JsonResponse({"success": "ok"})
            return JsonResponse(
                {"success": "form_error",
                 "errors": f"{form.errors}"}
            )
        return JsonResponse({"success": "ajax_error"})
        # categories = Category.objects.all()
        # foundations = Institution.objects.all()
        # form = DonationForm()
        # ctx = {
        #     "categories": categories,
        #     "foundations": foundations,
        #     "form": form
        # }
        # return render(request, 'form.html', ctx)


@login_required
def confirmation(request):
    return render(request, 'form-confirmation.html')


class Login(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect('main')
        return render(request,
                      'login.html',
                      {"form": LoginForm()}
                      )

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

        return render(request,
                      'register.html',
                      {"form": RegistrationForm()}
                      )

    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request,
                          'register.html',
                          {"form": form}
                          )
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['name']
        last_name = form.cleaned_data['surname']
        password = form.cleaned_data['password']
        password_2 = form.cleaned_data['password2']
        if password != password_2:
            messages.add_message(request, messages.WARNING, 'Błędnie powtórzone hasło. Spróbuj jeszcze raz.')
            return render(request,
                          'register.html',
                          {"form": form}
                          )
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.WARNING, 'Profil o podanym emailu już istnieje.')
            return render(request,
                          'register.html',
                          {"form": form}
                          )
        User.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                 last_name=last_name)
        return redirect('login')


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


# wyszukanie i wyświetlenie wszystkich datków danego użytkownika
class ProfileView(View, LoginRequiredMixin):
    def get(self, request):
        user = request.user
        user_institutions = {}
        donations = Donation.objects.filter(user=user)
        institutions = Institution.objects.all()
        for donation in donations:
            for institution in institutions:
                if donation.institution == institution:
                    user_donation_quantity = donations.filter(institution=donation.institution)
                    donation_quantity = user_donation_quantity.aggregate(Sum('quantity'))
                    if donation.institution.name not in user_institutions.keys():
                        user_institutions[donation.institution.name] = [
                            donation_quantity.get('quantity__sum'),
                            [category.name for category in donation.categories.all()]
                        ]

        ctx = {
            "user": user,
            "donations": donations,
            "user_institutions": user_institutions
        }
        return render(request, 'profile.html', ctx)
