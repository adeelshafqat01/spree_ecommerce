from django.urls import path
from .views import *

urlpatterns = [
    path("login", LoginUser.as_view(), name="Login"),
    path("register", RegisterUser.as_view(), name="Register"),
    path("viewusers", ViewAllUsers.as_view(), name="ViewUsers"),
    path("viewuser/<uuid:user_id>/", ViewUser.as_view(), name="ViewUser"),
    path("logout", Logout.as_view(), name="Logout"),
    path("resetpassword", ResetPassword.as_view(), name="reset-password"),
    path(
        "resetpasswordhandler",
        ResetPasswordHandler.as_view(),
        name="reset-password-handler",
    ),
]
