from django.db import models 

class User(models.Model):
    username = models.CharField(max_length=1000)
    email = models.EmailField()
    password = models.CharField(max_length=1000)
    role = models.CharField(max_length=1000)

class Token(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    token_value = models.CharField(max_length=1000)

class Auction(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_price = models.IntegerField(default=0)
    item_name = models.CharField(max_length=1000)
    winner_user_id = models.ForeignKey(User,on_delete=models.CASCADE)

class Bid(models.Model):
    auction_id = models.ForeignKey(Auction,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    bid_amount = models.IntegerField(default=0)
    timestamp = models.TimeField()
