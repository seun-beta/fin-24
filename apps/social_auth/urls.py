from django.urls import path

from apps.social_auth.views import (
    FacebookSocialAuthView,
    GoogleSocialAuthView,
    TwitterSocialAuthView,
)

urlpatterns = [
    path("social-auth/google/", GoogleSocialAuthView.as_view()),
    path("social-auth/facebook/", FacebookSocialAuthView.as_view()),
    path("social-auth/twitter/", TwitterSocialAuthView.as_view()),
]
