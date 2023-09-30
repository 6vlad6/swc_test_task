from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API Тестового задания",
        default_version='v1',
        description="API для работы с объектами Пользователя и События",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tymchukvladislav.work@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/events/', include('main.urls')),
    path('api/users/', include('authentication.urls')),
    path('', include('frontend.urls')),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
