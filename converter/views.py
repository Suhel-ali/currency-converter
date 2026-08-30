import requests

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    Profile,
    Conversion,
    Favourite,
    Feedback,
    ContactMessage
)


def get_currencies():

    try:

        response = requests.get(
            "https://api.frankfurter.dev/v2/currencies"
        )

        if response.status_code == 200:
            return response.json()

    except requests.RequestException:
        pass

    return []


# ---------------- HOME ----------------

def home(request):

    currencies = get_currencies()

    

    return render(
        request,
        "home.html",
        {
            "currencies": currencies
        }
    )
# ---------------- REGISTER ----------------

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not email or not password:
            return render(
                request,
                "register.html",
                {
                    "error": "Please fill all fields."
                }
            )

        if password != confirm_password:
            return render(
                request,
                "register.html",
                {
                    "error": "Passwords do not match."
                }
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {
                    "error": "Username already exists."
                }
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "register.html",
                {
                    "error": "Email already exists."
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user
        )

        login(request, user)

        return redirect("home")

    return render(request, "register.html")


# ---------------- LOGIN ----------------

# ---------------- LOGIN ----------------

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")


    # =========================================
    # GET REQUEST
    # =========================================

    if request.method == "GET":

        next_page = request.GET.get("next")

        message = None


        # User is trying to access favourites

        if next_page and next_page.startswith("/favourites"):

            message = (
                "You need to login to use "
                "Favourite Currencies."
            )


        # User is trying to access history

        elif next_page and next_page.startswith("/history"):

            message = (
                "You need to login to view "
                "your Conversion History."
            )


        # User is trying to access feedback

        elif next_page and next_page.startswith("/feedback"):

            message = (
                "You need to login to submit "
                "Feedback."
            )


        # User is trying to access profile

        elif next_page and next_page.startswith("/profile"):

            message = (
                "You need to login to view "
                "your Profile."
            )


        # User is trying to access contact

        elif next_page and next_page.startswith("/contact"):

            message = (
                "You need to login to Contact Us."
            )


        return render(
            request,
            "login.html",
            {
                "message": message,
                "next_page": next_page
            }
        )


    # =========================================
    # POST REQUEST
    # =========================================

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(
        request,
        username=username,
        password=password
    )


    if user is not None:

        login(request, user)

        next_page = request.POST.get("next")


        if next_page:

            return redirect(next_page)


        return redirect("home")


    # =========================================
    # INVALID LOGIN
    # =========================================

    return render(
        request,
        "login.html",
        {
            "error": "Invalid username or password.",
            "next_page": request.POST.get("next")
        }
    )
# ---------------- PROFILE ----------------

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        image = request.FILES.get("image")

        if image:

            profile.image = image
            profile.save()

        return redirect("profile")

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )


# ---------------- CONVERT CURRENCY ----------------


def convert_currency(request):

    if request.method != "POST":
        return redirect("home")

    amount = request.POST.get("amount")
    from_currency = request.POST.get("from_currency")
    to_currency = request.POST.get("to_currency")

    try:

        amount = float(amount)

        # Frankfurter API
        url = (
            f"https://api.frankfurter.dev/v2/rate/"
            f"{from_currency}/{to_currency}"
        )

        response = requests.get(url)
        currencies = get_currencies()

        if response.status_code != 200:

            return render(
                request,
                "home.html",
                {
                    "error": "Unable to get exchange rate."
                }
            )

        data = response.json()

        rate = data["rate"]

        # Calculate conversion
        converted_amount = amount * rate

        if request.user.is_authenticated:   
            Conversion.objects.create(
                user=request.user,
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                rate=rate,
                converted_amount=converted_amount
        )

        return render(
            request,
            "home.html",
            {   
                "currencies": currencies,
                "result": converted_amount,
                "rate": rate,
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
            }
        )

    except (ValueError, TypeError):

        return render(
            request,
            "home.html",
            {
                "error": "Please enter a valid amount."
            }
        )

    except requests.RequestException:

        return render(
            request,
            "home.html",
            {
                "error": "Unable to connect to Frankfurter."
            }
        )


# ---------------- HISTORY ----------------

@login_required
def history(request):

    conversions = Conversion.objects.filter(
        user=request.user
    ).order_by("-conversion_date")

    return render(
        request,
        "history.html",
        {
            "conversions": conversions
        }
    )


# ---------------- FAVOURITES ----------------

@login_required
def favourites(request):

    favourites = Favourite.objects.filter(
        user=request.user
    ).order_by("-added_date")

    return render(
        request,
        "favourites.html",
        {
            "favourites": favourites
        }
    )


# ---------------- ADD FAVOURITE ----------------
@login_required(login_url="/login/")
def add_favourite(request):

    try:

        if request.method == "POST":

            from_currency = request.POST.get("from_currency")
            to_currency = request.POST.get("to_currency")

            if from_currency and to_currency:

                Favourite.objects.get_or_create(
                    user=request.user,
                    from_currency=from_currency,
                    to_currency=to_currency
                )

    except Exception as e:

        print(f"Error adding favourite: {e}")

    return redirect("favourites")


# ---------------- REMOVE FAVOURITE ----------------

@login_required
def remove_favourite(request, favourite_id):

    if request.method == "POST":

        favourite = Favourite.objects.filter(
            id=favourite_id,
            user=request.user
        ).first()

        if favourite:
            favourite.delete()

    return redirect("favourites")

# ---------------- CONTACT ----------------

@login_required
def contact(request):

    if request.method == "POST":

        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not subject or not message:

            return render(
                request,
                "contact.html",
                {
                    "error": "Please fill all fields."
                }
            )

        ContactMessage.objects.create(
            user=request.user,
            subject=subject,
            message=message
        )

        return redirect("contact")

    return render(
        request,
        "contact.html"
    )
# ---------------- CONTACT ----------------

@login_required
def contact(request):

    if request.method == "POST":

        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not subject or not message:

            return render(
                request,
                "contact.html",
                {
                    "error": "Please fill all fields."
                }
            )

        ContactMessage.objects.create(
            user=request.user,
            subject=subject,
            message=message
        )

        return redirect("contact")

    return render(
        request,
        "contact.html"
    )
# ---------------- FEEDBACK ----------------

@login_required
def feedback(request):

    if request.method == "POST":

        comment = request.POST.get("comment")

        if not comment:
            return render(
                request,
                "feedback.html",
                {
                    "error": "Please enter your feedback."
                }
            )

        Feedback.objects.create(
            user=request.user,
            comment=comment
        )

        return redirect("feedback")

    return render(
        request,
        "feedback.html"
    )
    # ---------------- LOGOUT ----------------

def logout_view(request):

    logout(request)

    return redirect("home")