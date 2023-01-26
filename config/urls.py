import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings, yasg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('rest-api-auth/', include('rest_framework.urls')),
    path("api/v1/", include("src.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += yasg.urlpatterns
