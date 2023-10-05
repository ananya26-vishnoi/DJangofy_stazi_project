from django.db import models 
from django.utils import timezone
import pytz

class User(models.Model):
    username = models.CharField(max_length=1000)
    email = models.EmailField()
    password = models.CharField(max_length=1000)
    role = models.CharField(max_length=1000)

class Token(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    token_value = models.CharField(max_length=1000)

class Auction(models.Model):
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    start_price = models.IntegerField(default=0)
    item_name = models.CharField(max_length=1000)
    winner_user_id = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    @classmethod
    def get_current_auctions(cls):
        current_time_utc = timezone.now()

        # Set the timezone to Indian Standard Time (IST)
        ist_timezone = pytz.timezone('Asia/Kolkata')

        # Convert the current time to IST
        current_time_ist = current_time_utc.astimezone(ist_timezone)
        print(current_time_ist)
        # Filter auctions based on IST timings
        current_auctions = cls.objects.filter(
            start_time__lte=current_time_ist,
            end_time__gte=current_time_ist.astimezone(ist_timezone)  # Convert end_time to IST
        )
        return current_auctions

class Bid(models.Model):
    auction_id = models.ForeignKey(Auction,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    bid_amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(null=True,blank=True)
