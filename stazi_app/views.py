from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from dotenv import load_dotenv 
load_dotenv()
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import random
import string

@api_view(['POST'])
def create_user(request):
    if "username" not in request.data or "email" not in request.data or "password" not in request.data or "role" not in request.data:
        return Response({"error":"username, email, password, and role are required"},status=status.HTTP_400_BAD_REQUEST)
    
    username=request.data["username"]
    email=request.data["email"]
    password=request.data["password"]
    role=request.data["role"]

    if role!='admin' and role!='user' :
        return Response({"error":"role must be either admin or user"},status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({"error":"email already exists"},status=status.HTTP_400_BAD_REQUEST)
        
    user=User.objects.create(username=username,email=email,password=password,role=role)
    user.save()
    user_serializer=UserSerializer(user)
    return Response(user_serializer.data,status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_user(request):
    if "email" not in request.data:
        return Response({"error":"email is required"},status=status.HTTP_400_BAD_REQUEST)
    if "password" not in request.data:
        return Response({"error":"password is required"},status=status.HTTP_400_BAD_REQUEST)
    
    email=request.data["email"]
    password=request.data["password"]

    if not User.objects.filter(email=email, password=password).exists():
        return Response({"error":"email or password id wrong"},status=status.HTTP_400_BAD_REQUEST)
    
    # if "role" in request.data:
    #     role=request.data["role"]
    #     if role!='admin' and role!='user' :
    #         return Response({"error":"role must be either admin or user"},status=status.HTTP_400_BAD_REQUEST)
    #     User.objects.filter(email=email).update(role=role)

    if "new_password" in request.data:
        new_password=request.data["new_password"]
        User.objects.filter(email=email).update(password=new_password)

    if "username" in request.data:
        username=request.data["username"]
        User.objects.filter(email=email).update(username=username)
    user=User.objects.get(email=email)
    user_serializer=UserSerializer(user)
    return Response(user_serializer.data,status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request):
    if "email" not in request.data:
        return Response({"error":"email is required"},status=status.HTTP_400_BAD_REQUEST)
    if "password" not in request.data:
        return Response({"error":"password is required"},status=status.HTTP_400_BAD_REQUEST)
    
    email=request.data["email"]
    password=request.data["password"]

    if not User.objects.filter(email=email, password=password).exists():
        return Response({"error":"profile does not exist"},status=status.HTTP_400_BAD_REQUEST)
    user=User.objects.get(email=email)
    user.delete()
    return Response({"success":"user deleted"},status=status.HTTP_200_OK)

@api_view(['POST'])
def user_login(request):
    if "token_value" in request.data:
        token_value=request.data["token_value"]
        if Token.objects.filter(token_value=token_value).exists():
            token=Token.objects.get(token_value=token_value)
            user_id=token.user_id.id
            user=User.objects.get(id=user_id)
            user_serializer=UserSerializer(user)
            token_serializer=TokenSerializer(token)
            return Response({"user":user_serializer.data,"token":token_serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"token does not exist"},status=status.HTTP_400_BAD_REQUEST)
    if "email" not in request.data:
        return Response({"error":"email is required"},status=status.HTTP_400_BAD_REQUEST)
    if "password" not in request.data:
        return Response({"error":"password is required"},status=status.HTTP_400_BAD_REQUEST)
    
    email=request.data["email"]
    password=request.data["password"]

    if not User.objects.filter(email=email, password=password).exists():
        return Response({"error":"email or password id wrong"},status=status.HTTP_400_BAD_REQUEST)
    user=User.objects.get(email=email)
    token_value = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
    token=Token.objects.create(user_id=user,token_value=token_value)
    token.save()
    user_serializer=UserSerializer(user)
    token_serializer=TokenSerializer(token)
    return Response({"user":user_serializer.data,"token":token_serializer.data},status=status.HTTP_200_OK)
 
@api_view(['POST'])
def create_auction(request):
    if "start_time" not in request.data or "end_time" not in request.data or "start_price" not in request.data or "item_name" not in request.data:
        return Response({"error":"start_time, end_time, start_price, and item_name are required"},status=status.HTTP_400_BAD_REQUEST)
    
    start_time=request.data["start_time"]
    end_time=request.data["end_time"]
    start_price=request.data["start_price"]
    item_name=request.data["item_name"]

    auction=Auction.objects.create(start_time=start_time,end_time=end_time,start_price=start_price,item_name=item_name)
    auction.save()
    auction_serializer=AuctionSerializer(auction)
    return Response(auction_serializer.data,status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_auction(request):
    if "auction_id" not in request.data:
        return Response({"error":"auction_id is required"},status=status.HTTP_400_BAD_REQUEST)
    
    auction_id=request.data["auction_id"]

    if not Auction.objects.filter(id=auction_id).exists():
        return Response({"error":"auction does not exist"},status=status.HTTP_400_BAD_REQUEST)
    
    if "start_time" in request.data:
        start_time=request.data["start_time"]
        Auction.objects.filter(id=auction_id).update(start_time=start_time)

    if "end_time" in request.data:
        end_time=request.data["end_time"]
        Auction.objects.filter(id=auction_id).update(end_time=end_time)

    if "start_price" in request.data:
        start_price=request.data["start_price"]
        Auction.objects.filter(id=auction_id).update(start_price=start_price)

    if "item_name" in request.data:
        item_name=request.data["item_name"]
        Auction.objects.filter(id=auction_id).update(item_name=item_name)

    auction=Auction.objects.get(id=auction_id)
    auction_serializer=AuctionSerializer(auction)
    return Response(auction_serializer.data,status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_auction(request):
    if "auction_id" not in request.data:
        return Response({"error":"auction_id is required"},status=status.HTTP_400_BAD_REQUEST)
    
    auction_id=request.data["auction_id"]

    if not Auction.objects.filter(id=auction_id).exists():
        return Response({"error":"auction does not exist"},status=status.HTTP_400_BAD_REQUEST)
    auction=Auction.objects.get(id=auction_id)
    auction.delete()
    return Response({"success":"auction deleted"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user(request):
    if "token_value" not in request.data:
        return Response({"error":"token_value is required"},status=status.HTTP_400_BAD_REQUEST)
    tokenValue=request.data["token_value"]
    if not Token.objects.filter(token_value=tokenValue).exists():
        return Response({"error":"token does not exist"},status=status.HTTP_400_BAD_REQUEST)
    role = Token.objects.get(token_value=tokenValue)
    role=role.user_id.role

    if role !="admin":
        return Response({"error":"Not valid"},status=status.HTTP_400_BAD_REQUEST)
    
    if "user_ids" not in request.data:
        return Response({"error":"User ID does not exist"},status=status.HTTP_400_BAD_REQUEST)
    
    user_IDs=request.data["user_ids"]
    if type(user_IDs)!=list:
        return Response({"error":"user ID should be list"},status=status.HTTP_400_BAD_REQUEST)
    
    if len(user_IDs)==0:
        user=User.objects.all()
        user_serializer=UserSerializer(user,many=True)
        return Response (user_serializer.data,status=status.HTTP_200_OK)
    
    user = User.objects.filter(id__in=user_IDs)
    
    if len(user)>1:
        user_serializer=UserSerializer(user,many=True)
    else:
        user_serializer=UserSerializer(user)

    return Response(user_serializer.data,status=status.HTTP_200_OK)

    

    
