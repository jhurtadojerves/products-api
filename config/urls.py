"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView

from apps.accounts.authentication import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)
from apps.api.urls import urlpatterns_v1

urlpatterns = [
    path("", RedirectView.as_view(url="/api/docs/", permanent=True)),
    path("api/v1/", include(urlpatterns_v1)),
    path(
        "api/v1/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/v1/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/schema.json", SpectacularJSONAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema", template_name="api/swagger-ui.html"
        ),
        name="swagger-ui",
    ),
]
