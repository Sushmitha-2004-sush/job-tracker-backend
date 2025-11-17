from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, RegisterView

router = DefaultRouter()
router.register(r'applications', JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
