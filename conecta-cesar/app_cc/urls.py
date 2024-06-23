from django.urls import path
from . import views

urlpatterns = [
    # Rotas para Alunos
    path('aluno/avisos/', views.avisos, name='avisos'),
    path('aluno/avisos/<int:aviso_id>/', views.detalhe_aviso, name='detalhe_aviso'),
    path('aluno/forum_novo/', views.create_post, name='create_post'),
    path('apagar_post/<int:post_id>/', views.apagar_post, name='apagar_post'),
    path('aluno/forum/', views.forum_view, name='forum'),
    path('aluno/boletim/', views.boletim, name='boletim'),
    path('aluno/frequencia/', views.frequencia, name='frequencia'),
    path('aluno/perfil/', views.perfil, name='perfil'),
    path('aluno/diario/', views.diario, name='diario'),
    path('aluno/calendario/', views.calendario, name='calendario'),
    path('aluno/variacao_notas/', views.variacao_notas, name='variacao_notas'),
    path('aluno/hora_extra/', views.hora_extra, name='hora_extra'),
    path('aluno/slides/', views.slides, name="slides"),
    path('todo/', views.todo_list_view, name='todo_list'),
    path('todo/create/', views.create_todo_list, name='create_todo_list'),
    path('todo/<int:list_id>/add_item/', views.add_todo_item, name='add_todo_item'),
    path('todo/<int:list_id>/delete/', views.delete_todo_list, name='delete_todo_list'),
    path('todo/item/<int:item_id>/delete/', views.delete_todo_item, name='delete_todo_item'),
    path('aluno/vocorrencias/', views.vocorrencias, name='vocorrencias'),
    



    # Rotas para Professores
    path('professor/boletimp/', views.boletimp, name='boletimp'),
    path('professor/diariop/', views.diariop, name='diariop'),
    path('professor/perfilp/', views.perfilp, name='perfilp'),
    path('professor/frequenciap/', views.frequenciap, name='frequenciap'),
    path('professor/calendariop/', views.calendariop, name='calendariop'),
    path('professor/avisosp/', views.avisosp, name='avisosp'),
    path('professor/avisosp/<int:aviso_id>/', views.detalhe_avisop, name='detalhe_avisop'),
    path('professor/slidesp/', views.slidesp, name="slidesp"),
    path('professor/relatoriosp/', views.relatoriop, name="relatoriosp"),
    path('professor/ocorrenciasp/', views.ocorrenciasp, name="ocorrenciasp")

]
