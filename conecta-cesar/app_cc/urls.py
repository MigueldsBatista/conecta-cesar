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
    path('aluno/avisos', views.avisos, name='avisos'),
    path('aluno/boletim', views.boletim, name='boletim'),
    path('aluno/frequencia', views.frequencia, name='frequencia'),
    path('aluno/perfil', views.perfil, name='perfil'),
    path('aluno/diario', views.diario, name='diario'),
    path('aluno/calendario', views.calendario, name='calendario'),



    #Professor
    path('professor/boletimp', views.boletimp, name='boletimp'),
    path('professor/diariop', views.diariop, name='diariop'),
    path('professor/turmas', views.turmas, name='turmas'),
    path('professor/perfilp', views.perfilp, name='perfilp'),
    path('professor/frequenciap', views.frequenciap, name='frequenciap'),
    path('professor/calendariop', views.calendariop, name='calendariop'),
    path('professor/avisosp', views.avisosp, name='avisosp'),
    path('professor/disciplinas_e_notas', views.disciplinas_e_notas, name='disciplinas_e_notas'),
   

   
]
"""Todos os arquivos html é preciso definir o path aqui"""
