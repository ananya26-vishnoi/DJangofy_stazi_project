from rest_framework import serializers 
from .models import User
from .models import Token
from .models import Auction
from .models import Bid

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields = '__all__' 
class TokenSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Token 
        fields = '__all__' 
class AuctionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Auction 
        fields = '__all__' 
class BidSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Bid 
        fields = '__all__' 
