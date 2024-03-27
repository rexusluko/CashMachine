from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cash_machine.urls import router as cash_machine_router

api_router = DefaultRouter()
api_router.registry.extend(cash_machine_router.registry)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Browsable API Auth
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger docs
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    # The entire API
    path('api/v1/', include(api_router.urls)),
    path('', include('cash_machine.urls')),
]
