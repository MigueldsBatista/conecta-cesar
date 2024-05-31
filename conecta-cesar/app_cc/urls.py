from django.urls import path
from . import views

urlpatterns = [
    # Rotas para Alunos
    path('aluno/avisos/', views.avisos, name='avisos'),
    path('aluno/avisos/<int:aviso_id>/', views.detalhe_aviso, name='detalhe_aviso'),

    path('aluno/boletim/', views.boletim, name='boletim'),
    path('aluno/frequencia/', views.frequencia, name='frequencia'),
    path('aluno/perfil/', views.perfil, name='perfil'),
    path('aluno/diario/', views.diario, name='diario'),
    path('aluno/calendario/', views.calendario, name='calendario'),
    path('aluno/variacao_notas/', views.variacao_notas, name='variacao_notas'),
    path('aluno/hora_extra/', views.hora_extra, name='hora_extra'),

    # Rotas para Professores
    path('professor/boletimp/', views.boletimp, name='boletimp'),
    path('professor/diariop/', views.diariop, name='diariop'),
    path('professor/perfilp/', views.perfilp, name='perfilp'),
    path('professor/frequenciap/', views.frequenciap, name='frequenciap'),
    path('professor/calendariop/', views.calendariop, name='calendariop'),
    path('professor/avisosp/', views.avisosp, name='avisosp'),
    path('professor/slidesp', views.slidesp, name="slidesp"),
    path('professor/relatoriosp/', views.relatoriop, name="relatoriosp")
]
