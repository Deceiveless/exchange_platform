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
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from .spare_part import views as spare_part_views
from .statistics import views as statistics_views


api_router = routers.DefaultRouter()
api_router.register(r'spare-parts', spare_part_views.APIView)
api_router.register(r'model-stats', statistics_views.APIView)

urlpatterns = [
   url(r'^api/', include(api_router.urls)),

   url(r'^spare-part/?$', spare_part_views.FormView.as_view()),
   url(r'^spare-parts/?$', spare_part_views.ListView.as_view()),
   url(r'^model-stats/?$', statistics_views.ListView.as_view()),
   url(r'^$', spare_part_views.ListView.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
