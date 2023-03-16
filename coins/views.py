from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .utils import get_quote, get_historic_prices
from django.http import JsonResponse


def chart(request):
    labels = ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5"]
    data = [5, 10, 15, 20, 25]
    context = {
        "labels": labels,
        "values": data,
    }
    return render(request, "coins/chart.html", context)


def home(request):
    return render(request, "coins/index.html")


@login_required(login_url="/login_user")
def dashboard(request):
    if "firstname" in request.session:
        firstname = request.session["firstname"]

    if request.method == "POST":
        if "get_price" in request.POST:
            ticker = request.POST["ticker"]
            range_ = request.POST["range"]
            interval = request.POST["interval"]
            fundamentals = request.POST["fundamentals"]
            dividends = request.POST["dividends"]
            resultados = get_quote(ticker, range_, interval, fundamentals, dividends)
            price_data = get_historic_prices(ticker)
            
            return render(
                request,
                "coins/dashboard.html",
                {
                    "resultados": resultados,
                    "firstname": firstname,
                    "labels": price_data["labels"],
                    "data": price_data["data"],
                },
            )

    return render(request, "coins/dashboard.html", {"firstname": firstname})


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]

        if password1 != password2:
            messages.error(request, "Password does not match")
            return redirect("signup")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            messages.success(request, "User created successfully")
            user.save()
            return redirect("login_user")
    return render(request, "coins/signup.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["password1"]

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            request.session["firstname"] = firstname
            return redirect("dashboard")
    return render(request, "coins/login.html")


def signout(request):
    logout(request)
    return redirect("home")
