from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# from .models import User
from .serializers import UserSerializer, UsersSerializer

from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework.response import Response
from django.db.models import Count

from django.contrib.auth.models import User

# //verificar 
# from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login

# from django.contrib import auth
from django.contrib.auth.hashers import make_password

class UsersViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer



@csrf_exempt 
@api_view(['POST', 'GET'])
def UsersDetail(request):
    email_ = request.data.get('email')
    password_ =request.data.get('password')

    if email_:
        user_ = User.objects.get(email=email_, password=password_)
        # .get(password=password)        
        # print (str(user_.query))
        # return Response({"Datos": []})        
        # serializer = UsersSerializer(user_)
        # return Response(serializer.data)
        # user_ = User.objects.get(email=email_)
        # if user_.check_password(password_):
            # return Response({"validado": user_})
        # user_ = User.objects.get(password=password_)
        login(request, user_)
        serializer = UsersSerializer(user_)
        return Response(serializer.data)
        
        # user = authenticate(
        #         username=email_,
        #         password=password_
        #     )
        # print(user)

        # if user is not None:
        #     login(request, user)
        #     return Response({"validado": user})
        # else:
        #     return Response({"error": []})            

    else:
        return Response({"error": []})