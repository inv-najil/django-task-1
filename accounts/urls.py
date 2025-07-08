from django.urls import path
from .views import LoginAPIview,RegistrationAPIview

urlpatterns=[
    path('login/',LoginAPIview.as_view(),name='login'),
    path('register/',RegistrationAPIview.as_view(),name='register')
]