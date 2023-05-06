from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
import bcrypt
from rest_framework import status
from .models import User, Roles
from .serializers import UserSerializer
import json
from django.contrib.auth import login, logout
from .messages import *
from .jwttoken import get_tokens_for_user
from utils.email import send_email
from utils.generatetoken import ActivationTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.


class LoginUser(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated | HasAPIKey]

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if email is None or password is None:
            return Response(
                {"msg": EMAIL_PASSWORD_REQUIRED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email)
        except:
            return Response(
                {"msg": USER_NOT_VALID},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            if user.check_password(password):
                login(request, user)
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "msg": SUCCESS_LOGIN,
                        "refresh": token["refresh"],
                        "access": token["access"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": USER_NOT_VALID},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        admin_code = request.data.get("admin_code", None)
        if email is None or password is None:
            return Response(
                {"msg": EMAIL_PASSWORD_REQUIRED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email)
        except:
            if admin_code:
                user_roles = Roles.objects.get(user_roles="admin")
            else:
                user_roles = Roles.objects.get(user_roles="client")
            User.objects.create(email=email, password=password, roles=user_roles)
            return Response(
                {"msg": SUCCESS_REGISTER},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"msg": USER_ALREADY_EXISTS},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ViewAllUsers(APIView):
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get(self, request):
        user = request.user
        if user.roles.user_roles == "admin":
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            data = serializer.data
            return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"msg": "User not Verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(
            {"msg": LOGGED_OUT},
            status=status.HTTP_200_OK,
        )


class ViewUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        current_user = request.user
        if current_user.id != user_id and current_user.roles.user_roles != "admin":
            return Response(
                {"msg": "User not Verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UserSerializer(current_user)
        data = serializer.data
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", None)
        new_password = request.data.get("new_password", None)
        if email is None or new_password is None:
            return Response(
                {
                    "msg": EMAIL_PASSWORD_REQUIRED,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        users = list(User.objects.filter(email=email))
        if users:
            user = users[0]
            token = ActivationTokenGenerator()
            token_key = token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            encoded_password = urlsafe_base64_encode(force_bytes(new_password))
            send_email(token_key, user.email, uid, encoded_password)
            return Response(
                {
                    "msg": "Email Send Successfully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "msg": USER_NOT_EXIST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordHandler(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        reset_code = request.query_params.get("code", None)
        user_id = request.query_params.get("uuid", None)
        encoded_password = request.query_params.get("pass", None)
        if reset_code is None or user_id is None or encoded_password is None:
            return Response(
                {
                    "msg": "Code not Valid",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # get the password and reset it
        try:
            uid = force_str(urlsafe_base64_decode(user_id))
            new_password = force_str(urlsafe_base64_decode(encoded_password))
            user = User.objects.get(id=uid)
        except:
            return Response(
                {
                    "msg": "Code not Valid",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = ActivationTokenGenerator()
        if token.check_token(user, reset_code):
            hashed_password = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            )
            user.password = hashed_password
            user.save()
            return Response(
                {
                    "msg": "Password Changed",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "msg": "Token Not Verified",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
