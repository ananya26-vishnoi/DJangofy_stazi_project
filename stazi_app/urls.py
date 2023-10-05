from django.urls import path
from . import views

urlpatterns = [
    path('createUser', views.create_user, name='create_user'),
    path('updateUser',views.update_user,name="update_user"),
    path('deleteUser',views.delete_user,name="delete_user"),
    path('loginUser',views.user_login,name="user_login"),
    path('createAuction',views.create_auction,name="create_auction"),
    path('updateAuction',views.update_auction,name="update_auction"),
    path('deleteAuction',views.delete_auction,name="delete_auction"),
    path('getUsers',views.get_user,name="get_user"),
    path('getAuctions',views.get_auction,name="get_auction"),
    path('createBid',views.bid,name="bid"),
    path('getWinner',views.get_winner,name="get_winner")
]
