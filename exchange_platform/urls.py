"""exchange_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static


api_router = routers.DefaultRouter()
web_router = routers.DefaultRouter()
for router in [api_router, web_router]:
    router.register(r'spare-part', views.SparePartView)
    router.register(r'model-stats', views.ModelStatisticsView)

urlpatterns = [
   url(r'^api/', include(api_router.urls)),
   url(r'^$', views.SparePartView.as_view({'get': 'list'})),
   # url(r'^{}(?P<path>.*)$'.format(settings.STATIC_URL[1:]), serve, dict(insecure=True)),
   url(r'^', include(web_router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
