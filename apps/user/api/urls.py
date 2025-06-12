from django.urls import path, include

from apps.user.api.views import UserLoginView, UserProfileView, UserRegistrationView


urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/<int:id>/', UserProfileView.as_view(), name='user-profile')
]