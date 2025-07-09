from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import StudentView

router = DefaultRouter()
router.register('students',StudentView,basename='students')
urlpatterns=[
    path('',include(router.urls))
]