from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
import debug_toolbar

# Debug urls
urlpatterns = []

# for serving uploaded files on dev environment with django
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns = urlpatterns + [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
