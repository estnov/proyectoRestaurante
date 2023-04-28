
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from appRestaurante.View import views

schema_view = get_schema_view(
 openapi.Info(
title="API para predicción de la categoria de un comentario de un restaurante",
default_version='v1',
description="Es el API para predicción de la categoria de un comentario de un restaurante",
terms_of_service="https://www.google.com/policies/terms/",
license=openapi.License(name="BSD License"),
 ),
 public=True,
 permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    url(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),    
    url(r'^nuevasolicitud/$',views.Clasificacion.determinarCategoria),
    url(r'^predecir/',views.Clasificacion.predecir),
    url(r'^predecirIOJson/',views.Clasificacion.predecirIOJson),
    path('admin/', admin.site.urls),
    
]
