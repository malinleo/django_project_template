from django.contrib import admin
from django.urls import include, path

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
