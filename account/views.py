from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User

# Create your views here.

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            data = request.data

            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            password = data['password']
            re_password = data['re_password']

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(username=username).exists():
                        User.objects.create_user(
                            first_name=first_name,
                            last_name=last_name,
                            username=username,
                            password=password
                        )
                    else:
                        return Response(
                            {"error": "Username already exists"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {"error": "Password must be at least 8 characters long"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"error": "Password does not match"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {"error": "Something went wrong when trying to register account"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
