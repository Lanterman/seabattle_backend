import debug_toolbar

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth.models import Group

from . import settings, yasg


admin.site.unregister(Group)
admin.site.site_header = "Sea battle administration"
admin.site.site_title = "Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    # DRF auth
    path('rest-api-auth/', include('rest_framework.urls')),

    # Oauth2 
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),

    # Apps
    path("api/v1/", include("src.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += yasg.urlpatterns
