from django.urls import path, include

from django.contrib import admin

urlpatterns = [
    path("", include("wine_wiki.urls", namespace="wine-wiki")),
    path("admin/", admin.site.urls),
]
