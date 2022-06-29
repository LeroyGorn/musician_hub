from django.urls import path

from accounts.views import (ActivateAccount, LoginView, LogoutView,
                            ProfileView, SignUpView)

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", ActivateAccount.as_view(), name="activate"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
