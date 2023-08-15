from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from dotenv import load_dotenv
from django.utils import timezone
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Max

import random
import string

@api_view(['POST'])
def create_user(request):
    if "username" not in request.data or "email" not in request.data or "password" not in request.data:
        return Response({"error":"username, email, password, and role are required"},status=status.HTTP_400_BAD_REQUEST)
    
    username=request.data["username"]
    email=request.data["email"]
    password=request.data["password"]
    
    if User.objects.filter(email=email).exists():
        return Response({"error":"email already exists"},status=status.HTTP_400_BAD_REQUEST)
        
    user=User.objects.create(username=username,email=email,password=password,role="user")
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

