from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TeacherView

router = DefaultRouter()
router.register('teachers',TeacherView,basename='teacher')

urlpatterns = [
    path('',include(router.urls))
]