from django.contrib import admin
from rest_framework import routers
from incidents.app.views import (
    IncidentViewSet, 
    UserViewSet,
    GroupViewSet,
    MetricsAPIView,
    HealthAPIView,
    AuthView
)
from django.urls import path, include
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'incidents', IncidentViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', AuthView.as_view(), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('metrics/', MetricsAPIView.as_view(), name='metrics'),
    path('health/', HealthAPIView.as_view(), name='health'),
]
