from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_cc.models import Turma, Professor, Disciplina, Aluno, Diario, Nota, Falta,Aviso, Evento
from rolepermissions.roles import assign_role
from project_cc.roles import Professor as ProfessorRole, Aluno as AlunoRole
from django.db.utils import IntegrityError
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Cria dados de teste para Cypress: Professor, Turma, Disciplina e Aluno'

    def handle(self, *args, **kwargs):
        try:
            # Criação do usuário para o professor
            user_professor = User.objects.create_user(
                username='professor1', password='123', email='professor1@test.com'
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

            # Criação de um diário
            diario = Diario.objects.create(
                disciplina=disciplina, titulo="Título do Diário", texto="Descrição do Diário"
            )

            # Criação de uma nota para o aluno
            nota = Nota.objects.create(
                aluno=aluno, disciplina=disciplina, valor=6.0
            )

            # Adição de 8 faltas para o aluno em diferentes dias
            base_date = date.today()
            for i in range(9):#Faltas o suficiente para o aluno entrar pro relatório de desempenho
                falta_date = base_date - timedelta(days=i)
                Falta.objects.create(
                    aluno=aluno, data=falta_date, justificada=False, disciplina=disciplina
                )

            User.objects.create_superuser(
                username='adm', password='123', email='adm@test.com'
            )

            Aviso.objects.create(
                titulo = "E2E aviso",
                corpo = "testes automatizados"
            )
            
            Evento.objects.create(
                titulo = "titulo",
                descricao = "evento e2e",
                horario = "12:30",
                disciplina = disciplina,
                professor = professor,
                data = date.today()
            )
                    
            self.stdout.write(self.style.SUCCESS('Dados de teste criados com sucesso: Professor, Turma, Disciplina, Aluno, Diário, Nota , Aviso, Evento Faltas Superusuário'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Erro de integridade, os seguintes dados já existem no banco de dados: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar dados de teste: {str(e)}'))