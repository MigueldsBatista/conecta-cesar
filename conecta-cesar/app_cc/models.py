from django.db import models
from django.contrib.auth.models import User

# Modelo para Turma

User.add_to_class('role', models.CharField(max_length=50, default='Aluno', choices=[('Aluno', 'Aluno'), ('Professor', 'Professor')]))

# Modelo para Turmas
class Turma(models.Model):
    nome = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.nome
    
    # Método para obter as disciplinas associadas a esta turma
    def obter_disciplinas(self):
        return self.disciplinas.all()  # Retorna todas as disciplinas associadas a esta turma


# Modelo para Professores
class Professor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor', null=True)
    
    def __str__(self):
        return self.usuario.username
    
    # Filtro para disciplinas deste professor
    def disciplinas(self):
        return Disciplina.objects.filter(professor=self)


# Modelo para Disciplinas
class Disciplina(models.Model):
    nome = models.CharField(max_length=100, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="disciplinas", null=True)
    turmas = models.ManyToManyField(Turma, related_name="disciplinas")

    def __str__(self):
        return self.nome


# Modelo para Alunos
class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno", null=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos", null=True)

    def __str__(self):
        return f"({self.usuario.username})"

    # Filtro para disciplinas da turma deste aluno
    def disciplinas(self):
        return self.turma.obter_disciplinas()  # Obtém as disciplinas associadas à turma do aluno


# Modelo para Notas
class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="notas", null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="notas", null=True)
    valor = models.FloatField()

    def __str__(self):
        return f"{self.aluno.usuario.username} - {self.disciplina.nome}: {self.valor}"

class Diario(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='diarios', null=True)
    titulo = models.CharField(max_length=100, null=True)
    texto = models.TextField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.disciplina.nome} - {self.titulo}"
