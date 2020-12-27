from django.urls import path
from .views import SignupView, VerifyAccountView, UnverifiedAccountLoginView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('verify/reset/', UnverifiedAccountLoginView.as_view()),
    path('verify/', VerifyAccountView.as_view()),
]