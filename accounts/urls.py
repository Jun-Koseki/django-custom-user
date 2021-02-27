from django.urls import path
from .views import SignUpView, ProfileView, ChangePasswordView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password/', ChangePasswordView.as_view(), name='change_password')
]
