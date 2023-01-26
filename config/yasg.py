from django.urls import path, include
from rest_framework import permissions
from rest_framework.settings import api_settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


contact = openapi.Contact(name="Lanterman", url="https://github.com/Lanterman", email='klivchinskydmitry@gmail.com')

schema_url_patterns = [
   path("api/v1/", include('src.urls'))
]

schema_view = get_schema_view(
   openapi.Info(
      title="Sea Battle",
      default_version=api_settings.DEFAULT_VERSION,
      description="Test description",
      license=openapi.License(name="BSD License"),
      contact=contact,
   ),
   public=True,
   patterns=schema_url_patterns,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
