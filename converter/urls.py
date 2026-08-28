from django.urls import path

from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Currency Conversion
    path(
        "convert/",
        views.convert_currency,
        name="convert"
    ),

    # History
    path(
        "history/",
        views.history,
        name="history"
    ),

    # Register
    path(
        "register/",
        views.register,
        name="register"
    ),

    # Login
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    # Logout
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    # Favourites
    path(
        "favourites/",
        views.favourites,
        name="favourites"
    ),

    # Add Favourite
    path(
        "favourites/add/",
        views.add_favourite,
        name="add_favourite"
    ),

    # Remove Favourite
    path(
        "favourites/remove/<int:favourite_id>/",
        views.remove_favourite,
        name="remove_favourite"
    ),

    # Contact
    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    # Feedback
    path(
        "feedback/",
        views.feedback,
        name="feedback"
    ),

]