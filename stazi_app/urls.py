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
]
