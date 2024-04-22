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
    
    #aluno
    path('avisos', views.avisos, name='avisos'),
    path('boletim', views.boletim, name='boletim'),
    path('frequencia', views.frequencia, name='frequencia'),
    path('perfil', views.perfil, name='perfil'),
    path('diario', views.diario, name='diario'),
    path('calendario', views.calendario, name='calendario'),



    #Professor
    path('boletimp', views.boletimp, name='boletimp'),
    path('diariop', views.diariop, name='diariop'),
    path('turmas', views.turmas, name='turmas'),
    path('perfilp', views.perfilp, name='perfilp'),
    path('frequenciap', views.frequenciap, name='frequenciap'),
    path('calendariop', views.calendariop, name='calendariop'),
    path('avisosp', views.avisosp, name='avisosp'),
    path('disciplinas_e_notas', views.disciplinas_e_notas, name='disciplinas_e_notas'),
   

   
]
"""Todos os arquivos html é preciso definir o path aqui"""
