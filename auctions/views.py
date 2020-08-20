from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Bid, Auction_listing, Comment

class BidForm(forms.Form):
    new_price    = forms.IntegerField(label='New Bid',min_value=0)

def index(request):
    listings = Auction_listing.objects.all()
    return render(request, "auctions/index.html",{
        'listings':listings,
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

def listings(request):
    pass

def listing(request,listing_id):
    if listing_id <= len(Auction_listing.objects.all()):
        listing = Auction_listing.objects.get(pk=listing_id)
        # print(listing.listings_for_bids.all())
        if request.method=='POST':
            if request.user.is_authenticated:
                bid = Bid(price=int(request.POST['new_price']),user=request.user,
                    listing=listing)

                message=''
                last_bid = listing.listings_for_bids.last()
                total_bids = listing.listings_for_bids.all()
                print(total_bids)
                if len(total_bids)==1 :
                    if bid.price < last_bid.price:
                        message='Error, your bid must be larger than startig bid!'
                        bid_count=len(total_bids)
                        return render(request,'auctions/listing.html',{
                            'listing':listing,
                            'bid':last_bid,
                            'form':BidForm(request.POST),
                            'message':message,
                            'bid_count':bid_count,
                        })
                    elif len(total_bids)>=1 and bid.price > last_bid.price:
                        bid.save()
                        message=None
                        bid_count=len(total_bids)
                        # print(listing.listings_for_bids.all())
                        return render(request,'auctions/listing.html',{
                            'listing':listing,
                            'bid':bid,
                            'form':BidForm(),
                            'message':None,
                            'bid_count':bid_count,
                        })
                    else:
                        bid.save()
                        message=None
                        bid_count=len(total_bids)
                        # print(listing.listings_for_bids.all())
                        return render(request,'auctions/listing.html',{
                            'listing':listing,
                            'bid':bid,
                            'form':BidForm(),
                            'message':None,
                            'bid_count':bid_count,
                        })

            else:
                return HttpResponseRedirect(reverse('listing',args=[listing_id,]))
            # last_bid = listings_for_bids.objects.last(
        print(request.method)
        bid = Bid(price=int(listing.starting_bid),user=listing.user,listing=listing,
        start_time=listing.start_time)


        if not listing.listings_for_bids.all():
            bid.save()
        else:
            bid = listing.listings_for_bids.last()
        bid_count = len(listing.listings_for_bids.all())
        return render(request, 'auctions/listing.html', {
            'listing':listing,
            'bid':bid,
            'form':BidForm(),
            'bid_count':bid_count,
            })
