"""
URL configuration for project_cc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings #Para css e imagens
from django.conf.urls.static import static
from django.conf import settings
from app_cc import views
urlpatterns = [
    #Aluno patterns
    path('admin/', admin.site.urls),
    path('', include('app_cc.urls')),
    path('avisos.html', include('app_cc.urls')),
    path('disciplina.html', include('app_cc.urls')),
    path('boletim.html', include('app_cc.urls')),
    path('frequencia.html', include('app_cc.urls')),
    path('perfil', include('app_cc.urls')),
    path('diario.html', include('app_cc.urls')),


    #Professor patterns
    path('turmas.html', include('app_cc.urls')),
    path('calendariop.html', include('app_cc.urls')),
    path('avisosp.html', include('app_cc.urls')),
    path('perfilp.html', include('app_cc.urls')),
    path('frequenciap.html', include('app_cc.urls')),
    path('diariop.html', include('app_cc.urls')),

    

    #path("arquivo.html", include('app_cc.urls)) para toda nova página do html


    #static path

    
]
