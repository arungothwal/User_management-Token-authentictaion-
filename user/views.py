from django.shortcuts import render
from .models import MyUser
from rest_framework import status
from .serializers import MyUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from .utils import password_check
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny,IsAuthenticatedOrReadOnly
from django.db.models import Q


# Create your views here.
class CreateUser(APIView):
    def post(self, request):
        try:
            params = request.data
            passwd = params.get('password')
            try:
                password_check(passwd)
            except Exception as e:
                # print(e,"hello")
                return Response({'message': 'Must have 1 lowercase and 1 uppercase and 1 special character and length should greater than or equal to 8'},status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            user_email = params.get('email')
            email = EmailMessage("Hello","You signed up as a new user to our site.",to=[user_email])
            user = MyUserSerializer(data=params)
            if user.is_valid(raise_exception=True):
                userObj = user.save()
                userObj.set_password(params['password'])
                userObj.save()
                email.send()
            return Response( {'message':"signup succesfully.please check your mail"}, status=status.HTTP_200_OK,content_type='application/json')
        except Exception as e:
            print(e)
            return Response({'message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):
    def post(self,request):
        try:
            params = request.data
            try:
                user_exists = MyUser.objects.get(email=params['email'])
            except Exception as e:
                return Response({'message':'This email is not exists.Please signup first'},status=status.HTTP_400_BAD_REQUEST)
            if not user_exists.is_active:
                return Response(
                    {"message": "Your account is deactivated by the Admin. Contact to admin for the reactivation."},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer =MyUserSerializer(user_exists)
            try:
                user = authenticate(email=params['email'], password=params['password'])
                login(request, user)
            except:
                return Response({"message": "You enter the wrong credentials."}, status=status.HTTP_400_BAD_REQUEST)
            user.save()
            return Response({"message": "Logged in successfully.", "data": serializer.data, "token": user.create_jwt()}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Please enter correct credentials"}, status=status.HTTP_400_BAD_REQUEST)



class Logout(APIView):
    def post(self,request):
        try:
            logout(request)
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class Get_all_user(APIView):
    permission_classes = (IsAdminUser,IsAuthenticated)
    def get(self,request):
        try:
            data = MyUser.objects.all()
            serializer = MyUserSerializer(data,many=True)
            return Response({'message':"All user data",'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message':e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Change_password(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request):
        try:
            user_email = request.user.email
            params =request.data
            current_password =params['current_password']
            new_password =params['new_password']
            confirm_password = params['confirm_password']
            try:
                password_check(new_password)
            except Exception as e:
                # print(e,"hello")
                return Response({'message':'Must have 1 lowercase and 1 uppercase and 1 special character and length should greater than or equal to 8'},
                                 status=status.HTTP_400_BAD_REQUEST)
            if not new_password == confirm_password:
                return Response({'message':'New password and Confirm password is not matching.'},status=status.HTTP_400_BAD_REQUEST)
            user =authenticate(email = user_email,password=current_password)
            if user is None:
                return Response({"message": "Current password dosen't match with old password"},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfuly"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Search(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            SearchKeyword = request.GET['SearchKeyword']
            query = MyUser.objects.filter(Q(email__icontains=SearchKeyword) | Q(first_name__icontains=SearchKeyword))
            serializer = MyUserSerializer(query, many=True)
            return Response({"message": "All user data", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)



