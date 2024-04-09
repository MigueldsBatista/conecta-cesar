"""
URL configuration for project_cc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view()
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('avisos', views.avisos),
    path('boletim', views.boletim),
    path('boletimp', views.boletimp),
    path('diariop', views.diariop),
    path('frequencia', views.frequencia),
    path('turmas', views.turmas),
    path('perfilp', views.perfilp),
    path('frequenciap', views.frequenciap),
    path('calendariop', views.calendariop),
    path('avisosp', views.avisosp),
    path('disciplinas_e_notas', views.disciplinas_e_notas),
    path('perfil', views.perfil),
    path('diario', views.diario),
]

"""Todos os arquivos html é preciso definir o path aqui"""
