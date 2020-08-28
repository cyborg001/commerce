from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    url_image = models.CharField(max_length=100,blank=True)
    category = models.CharField(max_length=64,blank=True)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='auctions_for_user')
    start_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Bid(models.Model):
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='bids_for_user')
    start_time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Auction_listing,on_delete=models.CASCADE,related_name='bids_for_listing')

    def __str__(self):
        return '{:.2f}'.format(self.price)



class Comment(models.Model):
    comentario = models.TextField()
    start_time = models.DateTimeField( auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments_for_user')
    listing = models.ForeignKey(Auction_listing,on_delete=models.CASCADE, related_name='comments_for_listing')

    def __str__(self):
        return f'comment from {self.user}'

class Lista(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='listas_for_user')
    listing = models.ForeignKey(Auction_listing,on_delete=models.CASCADE,related_name='listas_for_listing')

    def __str__(self):
        return f'lista de {self.user} {self.id}'
