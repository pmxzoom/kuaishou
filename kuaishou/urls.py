"""kuaishou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from list import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.allstart),
    path('index.html',views.allstart),
    path('billboard.html',views.btable),
    path('movie.html',views.mtable),
    path('tube.html',views.ttable),
    path('tubeBar.html',views.bart),
    path('movieBar.html',views.barm),
    path('billboardBar.html',views.barb),
    path('tubepie.html', views.piet),
    path('moviepie.html', views.piem),
    path('billboardpie.html', views.pieb),
    path('tubefunnel.html', views.funnelt),
    path('moviefunnel.html', views.funnelm),
    path('billboardfunnel.html', views.funnelb),
    path('tubepictorialbar.html', views.pictorialbart),
    path('moviepictorialbar.html', views.pictorialbarm),
    path('billboardpictorialbar.html', views.pictorialbarb),
    path('tubeeffectscatter.html', views.effectscattert),
    path('movieeffectscatter.html', views.effectscatterm),
    path('billboardeffectscatter.html', views.effectscatterb),
    path('billboardWordcloud.html',views.wordb),
    path('movieWordcloud.html', views.wordm),
    path('tubeWordcloud.html', views.wordt),
    path('update',views.allupdate),
    path('file_down', views.file_down),
    path('file1_down', views.file1_down),
    path('file2_down', views.file2_down)
]
