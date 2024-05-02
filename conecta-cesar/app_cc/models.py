from django.db import models
from django.contrib.auth.models import User
import random

# Modelo para Turmas

User.add_to_class('role', models.CharField(max_length=50, default='Aluno', choices=[('Aluno', 'Aluno'), ('Professor', 'Professor')]))
def generate_unique_ra():
    while True:
        ra = str(random.randint(10**9, 10**10 - 1))  # Gera um RA de 10 dígitos
        if not Aluno.objects.filter(ra=ra).exists() and not Professor.objects.filter(ra=ra).exists():
            return ra

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
    email= models.EmailField(null=True, max_length=254)
    ra = models.CharField(max_length=10, unique=True, default=generate_unique_ra)  # Função explícita para RA

    
    
    def __str__(self):
        return self.usuario.username
    
    # Método para obter disciplinas associadas ao professor
    def disciplinas(self):
        return Disciplina.objects.filter(professor=self)  # Disciplinas deste professor

# Modelo para Disciplinas
class Disciplina(models.Model):
    nome = models.CharField(max_length=100, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="disciplinas", null=True)
    turmas = models.ManyToManyField(Turma, related_name="disciplinas")  # Muitas disciplinas em muitas turmas

    def __str__(self):
        return self.nome

# Modelo para Alunos
class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno", null=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos", null=True)
    email = models.EmailField(null=True, max_length=254)  # Garantir emails únicos
    ra = models.CharField(max_length=10, unique=True, default=generate_unique_ra)
     
     # Função explícita para RA

    
    def __str__(self):
        return f"{self.usuario.username}"

    # Método para obter disciplinas associadas à turma do aluno
    def disciplinas(self):
        return self.turma.obter_disciplinas()  # Disciplinas associadas à turma


# Modelo para Notas
class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="notas", null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="notas", null=True)
    valor = models.FloatField(null=True, default='0')

    def __str__(self):
        return f"{self.aluno.usuario.username} - {self.disciplina.nome}: {self.valor}"
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Diario(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='diarios', null=True)
    titulo = models.CharField(max_length=100, null=True)
    texto = models.TextField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.disciplina.nome} - {self.titulo}"
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Falta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='faltas')
    data = models.DateField()
    justificada = models.BooleanField(default=False)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='faltas', null=True)  # Relacionamento com Disciplina
    def __str__(self):
        return f"Falta de {self.aluno.usuario.username} em {self.data}"
    
class File(models.Model):
    title=models.CharField(max_length=20, null=True)
    archive=models.ImageField()
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="arquivos", null=True)  # Relacionamento com Aluno
    horas_extras = models.FloatField(default=0)  # Campo para armazenar horas extras

    def __str__(self):
        return f"{self.title} - {self.aluno.usuario.username}"