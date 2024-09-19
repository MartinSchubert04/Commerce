from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Categories", views.Cats, name="Categories"),
    path("CreateListing", views.CreateListing, name="CreateListing"),
    path("Listing/<int:id>", views.showListing, name="showListing"),
    path("add/<int:id>", views.add, name="addWatchlist"),
    path("remove/<int:id>", views.remove, name="removeWatchlist"),  
    path("Watchlist", views.Watchlist, name="Watchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("newBid/<int:id>", views.newBid, name="newBid"),
    path("close/<int:id>", views.close, name="close"),
]
