from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin

urlpatterns = [
    path("", include("wine_wiki.urls", namespace="wine-wiki")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()
