from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (CategoryCreateView, CategoryDeleteView,
                       CategoryDetailView, CategoryUpdateView, PostDetailView,
                       PostListView, UserViewSet)

app_name = "api"

router = routers.DefaultRouter()
router.register("customers", UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Forum API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger_docs"),
    path("<uuid:uuid>/", PostDetailView.as_view(), name="post"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("category-create/", CategoryCreateView.as_view(), name="cat-create"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category"),
    path("category/<int:pk>/category-delete/", CategoryDeleteView.as_view(), name="category-delete"),
    path("category/<int:pk>/category-update/", CategoryUpdateView.as_view(), name="category-update"),
]
