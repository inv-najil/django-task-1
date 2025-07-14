from django.urls import path
from .views import LoginAPIview,RegistrationAPIview, PasswordRestRequestView, PasswordRestConfirmView

urlpatterns=[
    path('login/',LoginAPIview.as_view(),name='login'),
    path('register/',RegistrationAPIview.as_view(),name='register'),
    path('password-rest', PasswordRestRequestView.as_view(), name='password-rest'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordRestConfirmView.as_view(),name='password_rest_confirm')
]