from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_cc.models import Turma, Professor, Disciplina, Aluno, Diario, Nota, Falta, Aviso, Evento, ProfessorFile
from rolepermissions.roles import remove_role
from project_cc.roles import Professor as ProfessorRole, Aluno as AlunoRole
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Exclui dados de teste para Cypress: Professor, Turma, Disciplina, Aluno, Diário, Nota, Faltas, Avisos, Eventos e Arquivos do Professor'

    def handle(self, *args, **kwargs):
        try:
            # Exclui as faltas
            Falta.objects.filter(aluno__usuario__username='aluno1').delete()

            # Exclui as notas
            Nota.objects.filter(aluno__usuario__username='aluno1').delete()

            # Exclui os diários
            Diario.objects.filter(disciplina__nome='Disciplina 1').delete()

            # Exclui os alunos
            aluno = Aluno.objects.filter(usuario__username='aluno1').first()
            if aluno:
                remove_role(aluno.usuario, AlunoRole)
                aluno.usuario.delete()
                aluno.delete()

            # Exclui as disciplinas
            Disciplina.objects.filter(nome='Disciplina 1').delete()

            # Exclui as turmas
            Turma.objects.filter(nome='Turma 1').delete()

            # Exclui os professores
            professor = Professor.objects.filter(usuario__username='professor1').first()
            if professor:
                # Exclui os eventos associados ao professor
                Evento.objects.filter(professor=professor).delete()

                # Exclui os arquivos do professor
                ProfessorFile.objects.filter(professor=professor).delete()

                remove_role(professor.usuario, ProfessorRole)
                professor.usuario.delete()
                professor.delete()

            # Exclui os avisos
            Aviso.objects.filter(titulo='E2E aviso').delete()

            # Exclui o superusuário
            User.objects.filter(username='adm').delete()

            self.stdout.write(self.style.SUCCESS('Dados de teste excluídos com sucesso: Professor, Turma, Disciplina, Aluno, Diário, Nota, Faltas, Avisos, Eventos, Arquivos do Professor e Superusuário'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Erro ao excluir dados de teste: {str(e)}'))
