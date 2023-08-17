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

