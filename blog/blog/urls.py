"""
Blog loyihasining URL konfiguratsiyasi.

`urlpatterns` ro'yxati URL'larni view'lar bilan bog'laydi. Qo'shimcha ma'lumot uchun:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Misollar:
Funksiyalarga asoslangan view'lar:
    1. Import qo'shish:  from my_app import views
    2. URL'ni urlpatterns'ga qo'shish:  path('', views.home, name='home')

Sinflarga asoslangan view'lar:
    1. Import qo'shish:  from other_app.views import Home
    2. URL'ni urlpatterns'ga qo'shish:  path('', Home.as_view(), name='home')

Boshqa URL konfiguratsiyasini qo'shish:
    1. include() funksiyasini import qilish: from django.urls import include, path
    2. URL'ni urlpatterns'ga qo'shish:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API hujjatini yaratish
schema_view = get_schema_view(
   openapi.Info(
      title="Online Ta'lim API",
      default_version='v1',
      description="API uchun tavsif",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="shaxobiddinnormatov2@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneli uchun yo'l
    path('api/v1/', include('main.urls', namespace="v1")),  # 1-versiya API uchun URL konfiguratsiyasi
    path('api/v2/', include('main.urls', namespace="v2")),  # 2-versiya API uchun URL konfiguratsiyasi
    path('api-auth/', include('rest_framework.urls')),  # Avtomatik autentifikatsiya sahifalari

    # Swagger va Redoc interfeysi uchun yo'llar
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
