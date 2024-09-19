from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Categories, Listing, Comments, Bid


def index(request):
    active = Listing.objects.filter(activeState=True)

    if active is not None:
        return render(request, "auctions/index.html", {
            "listings": active
        })
    else:
        return render(request, "auctions/index.html", {
            "message": "There are no listings"
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def CreateListing(request):
    if request.method == "GET":
        categories = Categories.objects.all()
        return render(request, "auctions/CreateListing.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        category = Categories.objects.get(category=request.POST["category"])
        price = request.POST["price"]
        image = request.POST["image"]
        user = request.user
        categories = Categories.objects.all()


        if not price:
            return render(request, "auctions/CreateListing.html", {
            "categories": categories,
            "message": "There has to be an inicial price"
        })
        if not title:
            return render(request, "auctions/CreateListing.html", {
            "categories": categories,
            "message": "There has to be a title"
        })
        if not description:
            return render(request, "auctions/CreateListing.html", {
            "categories": categories,
            "message": "There has to be a description"
        })
        if len(description) > 300:
            return render(request, "auctions/CreateListing.html", {
            "categories": categories,
            "message": "The description must be 300 characters or less"
        })

        if not image:
            image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZlKDSCN5mBQ0Fdo8xunegZ4fOak5angiqsnIAnVtj4g&s"
        
        bid = Bid(bid=float(price), userBid=user)
        bid.save()

        newListing = Listing(
            title=title,
            description= description,
            inicialBid= bid,
            category=category,
            image=image,
            user=user,
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))

def Cats(request):
    if request.method == "GET":
        categories = Categories.objects.all()
        return render(request, "auctions/categories.html", {
            "categories": categories
        })
    else:
        formCat = request.POST["category"]
        userCat = Categories.objects.get(category=formCat)
        filtredListings = Listing.objects.filter(activeState=True, category=userCat)
        categories = Categories.objects.all()
        if not filtredListings:
            return render(request, "auctions/categories.html", {
            "message": "No listings in this category yet.",
            "categories": categories,
        })
        return render(request, "auctions/categories.html", {
            "categories": categories,
            "listings": filtredListings
        })
    
def showListing(request, id):
    data = Listing.objects.get(pk=id)
    inWatchlist = request.user in data.watchlist.all()
    comments = Comments.objects.filter(listingComment=data)
    owner = request.user == data.user

    return render(request, "auctions/showListing.html", {
        "listing": data,
        "inWatchlist": inWatchlist,
        "commentsInListing": comments,
        "listingOwner": owner,
    } 
    )

def remove(request, id):
    data = Listing.objects.get(pk=id)
    user = request.user
    data.watchlist.remove(user)   
    return HttpResponseRedirect(reverse("showListing", args=[id]))    
def add(request, id):
    data = Listing.objects.get(pk=id)
    user = request.user
    data.watchlist.add(user)   
    return HttpResponseRedirect(reverse("showListing", args=[id]))    

@login_required(login_url='login')
def Watchlist(request):
    user = request.user
    listings = user.userWatchlist.all()
    if not listings:
        return render (request, "auctions/watchlist.html", {
        "message2": "No elements in watchlist."
    })
    return render (request, "auctions/watchlist.html", {
        "listings": listings,
    })

def comment(request, id):
    user = request.user
    data = Listing.objects.get(pk=id)
    commentText = request.POST["addComment"]

    if not commentText:
        return HttpResponseRedirect(reverse("showListing", args=[id]))    

    newComment = Comments(
        userComment = user,
        listingComment = data,
        commentText = commentText
    )

    newComment.save()
    return HttpResponseRedirect(reverse("showListing", args=[id]))    

def newBid(request, id):
    potentialBid = request.POST['newBid']
    data = Listing.objects.get(pk=id)
    user = request.user
    comments = Comments.objects.filter(listingComment=data)
    owner = request.user.username == data.user.user


    if user == data.user:
        return render (request, "auctions/showListing.html", {
        "listing": data,
        "messageError": "You can not bid in your own listing",
        "commentsInListing": comments,
        "listingOwner": owner,

        })
    if float(potentialBid) > data.inicialBid.bid:
        newBid = Bid(userBid=user, bid=float(potentialBid))
        newBid.save()
        data.inicialBid = newBid
        data.save()
        return render (request, "auctions/showListing.html", {
            "listing": data,
            "message2": "Bidded successfully",
            "commentsInListing": comments,
            "listingOwner": owner,
        })   
    else:
        return render (request, "auctions/showListing.html", {
            "listing": data,
            "messageError": "Failed bid (the bid must be greater than the current one)",
            "commentsInListing": comments,
            "listingOwner": owner,
        })    

def close(request, id):
    data = Listing.objects.get(pk=id)
    data.activeState = False
    data.save()
    inWatchlist = request.user in data.watchlist.all()
    comments = Comments.objects.filter(listingComment=data)
    owner = request.user == data.user

    return render (request, "auctions/showListing.html", {
            "listing": data,
            "inWatchlist": inWatchlist,
            "commentsInListing": comments,
            "listingOwner": owner,
            "message": "Your auctions has been closed"
        }) 



