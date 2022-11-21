from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.settings.base import ADMIN_URL
from apps.incomes.urls import router as incomes_router
from apps.incomes.urls import urlpatterns as incomes_urlpatterns
from apps.expenses.urls import router as expenses_router
from apps.expenses.urls import urlpatterns as expenses_urlpatterns
from apps.users.urls import urlpatterns as users_urlpatterns
from apps.social_auth.urls import urlpatterns as social_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Fin-24 API",
        default_version="v1",
        description="Personal Finance Manager",
        contact=openapi.Contact(email="adegokeseunfunmi1999@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



if settings.DEBUG:
    urlpatterns = [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
else:
    urlpatterns = []


urlpatterns += [
    path(f"{ADMIN_URL}/", admin.site.urls),
    path("incomes/", include(incomes_router.urls)),
    path("expenses/", include(expenses_router.urls)),
]

urlpatterns.extend(users_urlpatterns)
urlpatterns.extend(incomes_urlpatterns)
urlpatterns.extend(expenses_urlpatterns)
urlpatterns.extend(social_urlpatterns)
