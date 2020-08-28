from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import BidForm, AuctionForm, CommentForm
from .models import User, Bid, Auction_listing, Comment, Lista
from django.contrib.auth.decorators import login_required


def index(request):
    listings = Auction_listing.objects.filter(is_active=True)
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

    listings = Auction_listing.objects.all()
    listing = listings.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)


    if request.method=='POST':
        if request.user.is_authenticated:
            if listing.bids_for_listing.all():

                bid_count = len(listing.bids_for_listing.all())
                last_bid = listing.bids_for_listing.last()
                bid = Bid(price=int(request.POST['new_price']),user=request.user,
                        listing=listing)
                if bid.price <= last_bid.price:
                    message='Error, your bid must be larger than last bid!'
                    form = BidForm(request.POST)
                    return render(request, 'auctions/listing.html', {
                        'listing':listing,
                        'bid':last_bid,
                        'form':form,
                        'bid_count':bid_count,
                        'message':message,
                        'comments':comments,
                        'commentform':CommentForm(),
                        })
                else:
                    bid.save()
                    message=None
                    form=BidForm()
                    return render(request, 'auctions/listing.html', {
                        'listing':listing,
                        'bid':bid,
                        'form':form,
                        'bid_count':bid_count,
                        'message':message,
                        'comments':comments,
                        'commentform':CommentForm(),
                        })
            else:
                bid = Bid(price=int(request.POST['new_price']),user=request.user,
                        listing=listing)
                bid_count = 0
                if bid.price < listing.price:
                    message='Error, your bid must be equal or larger than startig bid!'
                    form = BidForm(request.POST)
                    return render(request, 'auctions/listing.html', {
                        'listing':listing,
                        'bid':None,
                        'form':form,
                        'bid_count':bid_count,
                        'message':message,
                        'comments':comments,
                        'commentform':CommentForm(),
                        })
                else:
                    bid.save()
                    message=None
                    bid_count = 1
                    form = BidForm()
                    return render(request, 'auctions/listing.html', {
                        'listing':listing,
                        'bid':bid,
                        'form':form,
                        'bid_count':bid_count,
                        'message':message,
                        'comments':comments,
                        'commentform':CommentForm(),
                        })

    if listing.bids_for_listing.all():
        bid = listing.bids_for_listing.last()
    else:
        bid = None

    bid_count = len(listing.bids_for_listing.all())
    form = BidForm()
    return render(request, 'auctions/listing.html', {
        'listing':listing,
        'bid':bid,
        'form':form,
        'bid_count':bid_count,
        'message':None,
        'comments':comments,
        'commentform':CommentForm(),
        })


@login_required
def create_listing(request):
    if request.method=='POST':
        title = request.POST['title']
        description = request.POST['description']
        if request.POST['url_image'] != None:
            url_image = request.POST['url_image']
        if request.POST['category'] != None:
            category = request.POST['category']
        price = request.POST['starting_bid']
        user = request.user

        listing = Auction_listing(title=title, description=description, category=category,
            url_image=url_image, price=price,user=user)
        listing.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'auctions/create_listing.html', {
        'form':AuctionForm(),
    })

@login_required
def whatchlist(request):
    if not request.user.listas_for_user.all():
        return render(request, 'auctions/watchlist.html', {
            'listas':request.user.listas_for_user.all(),
        })

    return render(request, 'auctions/watchlist.html', {
        'listas':request.user.listas_for_user.all(),
    })

@login_required
def addLista(request,listing_id):

    listing = Auction_listing.objects.get(pk=listing_id)
    lista = Lista(user=request.user,listing=listing)
    listas = request.user.listas_for_user.all()
    for l in listas:
        if lista.listing.title == l.listing.title and \
        lista.listing.description == l.listing.description:
            return HttpResponseRedirect(reverse('listing',args=[listing_id,]))

    lista.save()
    return HttpResponseRedirect(reverse('listing',args=[listing_id,]))

@login_required
def remove_from_list(request, listing_id):
        listing = Auction_listing.objects.get(pk=listing_id)
        lista = request.user.listas_for_user.get(listing=listing)
        lista.delete()
        return HttpResponseRedirect(reverse('watchlist'))

@login_required
def close(request,listing_id):
    listing = Auction_listing.objects.get(pk=listing_id)
    bid = listing.bids_for_listing.last()
    print(bid)
    if listing.is_active == True and listing in request.user.auctions_for_user.all():
        listing.is_active=False
        listing.save()
    return HttpResponseRedirect(reverse('listing',args=[listing_id,]))

    # return HttpResponseRedirect(reverse('index'))

@login_required
def comment_view(request,listing_id):
    listing = Auction_listing.objects.get(pk=listing_id)
    if request.method=='POST':
        print('esto es un post')
        commentform = CommentForm(request.POST)
        print(commentform)
        if commentform.is_valid():
            comentario = request.POST['comentario']
            comment = Comment(comentario=comentario, user= request.user ,
                listing=listing)
            comment.save()

    return HttpResponseRedirect(reverse('listing', args=[listing_id,]))

def categories(request):
    listings = Auction_listing.objects.filter(is_active=True)
    for n in listings:
        print(n.category)
    categorias = {listing.category for listing in listings}
    for listing in listings:
        if listing.url_image != '':
            listing.url_image = '/auctions/'+listing.url_image
            print(listing.url_image)
    return render(request,'auctions/categories.html',{
        'listings':listings,
        'categorias':categorias,
    })
def categoria(request,categoria):
    if categoria == '':
        categoria = 'Variados'
    listings = Auction_listing.objects.filter(category=categoria)
    for listing in listings:
        if listing.url_image != '':
            listing.url_image = '/auctions/'+listing.url_image

    return render(request, 'auctions/category.html', {
        'listings': listings,
        'categorias':[categoria,],
    })
