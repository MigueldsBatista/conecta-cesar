from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_cc.models import Aluno, Falta, Disciplina
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Adiciona 8 faltas para um aluno específico baseado no nome de usuário'

    def handle(self, *args, **kwargs):
        username = input("Digite o nome de usuário do aluno: ")
        
        try:
            user = User.objects.get(username=username)
            aluno = Aluno.objects.get(usuario=user)
            disciplina = Disciplina.objects.filter(turmas=aluno.turma).first()

            if not disciplina:
                self.stdout.write(self.style.ERROR('Nenhuma disciplina encontrada para a turma do aluno.'))
                return

            base_date = date.today()
            for i in range(8):
                falta_date = base_date - timedelta(days=i)
                Falta.objects.create(
                    aluno=aluno, data=falta_date, justificada=False, disciplina=disciplina
                )

            self.stdout.write(self.style.SUCCESS(f'8 faltas adicionadas para o aluno: {username}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuário com nome de usuário "{username}" não encontrado.'))
        except Aluno.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Aluno com nome de usuário "{username}" não encontrado.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao adicionar faltas: {str(e)}'))
