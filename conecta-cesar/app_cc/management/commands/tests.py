from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_cc.models import Turma, Professor, Disciplina, Aluno
from rolepermissions.roles import assign_role
from project_cc.roles import Professor as ProfessorRole, Aluno as AlunoRole

class Command(BaseCommand):
    help = 'Cria dados de teste para Cypress: Professor, Turma, Disciplina e Aluno'

    def handle(self, *args, **kwargs):
        # Criação do usuário para o professor
        user_professor = User.objects.create_user(
            username='professor1', password='123', email='prof1@test.com'
        )

        # Criação do professor e associação ao usuário
        professor = Professor.objects.create(
            usuario=user_professor, ra='1234567890'
        )
        assign_role(user_professor, ProfessorRole)
        # Criação de uma turma
        turma = Turma.objects.create(nome='Turma 1')

        # Criação de uma disciplina e associação ao professor e à turma
        disciplina = Disciplina.objects.create(
            nome='Disciplina 1', professor=professor
        )
        disciplina.turmas.add(turma)

        # Criação de um aluno e associação à turma
        user_aluno = User.objects.create_user(
            username='aluno1', password='123', email='aluno1@test.com'
        )
        aluno = Aluno.objects.create(
            usuario=user_aluno, turma=turma, ra='0987654321'
        )
        assign_role(user_aluno, AlunoRole)
        self.stdout.write(self.style.SUCCESS('Dados de teste criados com sucesso: Professor, Turma, Disciplina e Aluno'))
