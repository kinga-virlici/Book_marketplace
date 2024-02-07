from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from account.forms import RegisterForm


#in acest fisier vom crea clase, metode sau functii cu ajutorul carora putem gestiona cererile HTTP ptimite de la utilizator

class LoginView(AuthLoginView):          #aceasta clasa moesteneste clasa AuthLoginView() si ne ofera functionalitatea de login,
    template_name = 'account/login.html' #aceasta clasa ne ofera sablonul personalizat pt pagina de login a aplicatiei


class LogoutView(AuthLogoutView):         #aceasta clasa moesteneste clasa AuthLogoutView() si ne ofera functionalitatea de logout
    template_name = 'account/logout.html' #aceasta clasa ne ofera sablonul personalizat pt pagina de logout a aplicatiei


def register(request):          # functia gestioneaza cererile GET - ne afiseaza formularul si POST - ne salveaza noul utilizator in baza de date
    if request.method == "GET":
        form = RegisterForm
        context = {
            "form": form
        }
        return render(request, 'account/register.html', context=context)
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

            return redirect('/')

