from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    url_image = models.CharField(max_length=100,blank=True)
    category = models.CharField(max_length=64,blank=True)
    starting_bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='users_for_auctions')
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} {self.start_time}'

class Bid(models.Model):
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='users_for_bids')
    start_time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Auction_listing,on_delete=models.CASCADE,related_name='listings_for_bids')

    def __str__(self):
        return '{:.2f}'.format(self.price)



class Comment(models.Model):
    comentario = models.TextField()
    start_time = models.DateTimeField( auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='users_for_comments')
    listing = models.ForeignKey(Auction_listing,on_delete=models.CASCADE, related_name='listings_for_comments')
