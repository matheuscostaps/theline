from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from theline.views import ClienteViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet) 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('theline.urls')), 
]