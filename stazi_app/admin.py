from django.contrib import admin 
from .models import User
from .models import Token
from .models import Auction
from .models import Bid

admin.site.register(User)
admin.site.register(Token)
admin.site.register(Auction)
admin.site.register(Bid)
