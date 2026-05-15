from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("browsing/", include("browsing.urls", namespace="browsing")),
    path("", include("webpage.urls", namespace="webpage")),
]
handler404 = "webpage.views.handler404"
