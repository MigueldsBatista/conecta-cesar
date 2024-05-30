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
    foto_perfil = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Novo campo de foto de perfil

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

    def obter_sigla(self):
        # Divide o nome por espaços e pega a primeira letra de cada palavra
        return "".join([palavra[0].upper() for palavra in self.nome.split()])

  
# Modelo para Alunos
class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno", null=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos", null=True)
    email = models.EmailField(null=True, max_length=254)  # Garantir emails únicos
    ra = models.CharField(max_length=10, unique=True, default=generate_unique_ra)
    foto_perfil = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Novo campo de foto de perfil

     
     # Função explícita para RA

    
    def __str__(self):
        return f"{self.usuario.username}"

    # Método para obter disciplinas associadas à turma do aluno
    def disciplinas(self):
        return self.turma.obter_disciplinas()  # Disciplinas associadas à turma

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data = models.DateField()
    horario = models.TimeField(blank=True, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.data}"
    
class Aviso(models.Model):
    titulo = models.CharField(max_length=200)
    corpo = models.TextField()
    publicado = models.DateTimeField(auto_now_add=True)
    imagem=models.ImageField(null=True, upload_to="images/" )

    def __str__(self):
        return self.titulo
    

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
        return f"Falta de {self.aluno.usuario.username} em {self.data}"#nao aparece pro usuario.
    
class File(models.Model):
    title=models.CharField(max_length=300, null=True)#Considerar deletar o título para evitar error
    archive=models.ImageField()
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="arquivos", null=True)  # Relacionamento com Aluno
    horas_extras = models.FloatField(default=0)  # Campo para armazenar horas extras

    def __str__(self):
        return f"{self.title} - {self.aluno.usuario.username}"
   
# Modelo de Relatório
class Relatorio(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='relatorios')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='relatorios', null=True)
    alunos_nota_abaixo = models.ManyToManyField(Aluno, related_name='relatorios_nota_abaixo', through='NotaRelatorio')
    alunos_frequencia_abaixo = models.ManyToManyField(Aluno, related_name='relatorios_frequencia_abaixo', through='FaltaRelatorio')

    def atualizar_relatorio(self, disciplina):
        # Reseta as listas de alunos
        self.alunos_nota_abaixo.clear()
        self.alunos_frequencia_abaixo.clear()

        # Verifica notas abaixo de 7 na disciplina específica
        notas = Nota.objects.filter(disciplina=disciplina, valor__lt=7)
        for nota in notas:
            nota_relatorio, created = NotaRelatorio.objects.get_or_create(relatorio=self, aluno=nota.aluno)
            nota_relatorio.nota = nota.valor
            nota_relatorio.save()
            self.alunos_nota_abaixo.add(nota.aluno)

        # Verifica faltas acima de 8 para todos os alunos na disciplina específica
        
        for aluno in Aluno.objects.filter(turma__disciplinas=disciplina):
            total_faltas = Falta.objects.filter(aluno=aluno, disciplina=disciplina).count()
            if total_faltas > 0:
                falta_relatorio, created = FaltaRelatorio.objects.get_or_create(relatorio=self, aluno=aluno)
                falta_relatorio.faltas = total_faltas
                falta_relatorio.save()
                self.alunos_frequencia_abaixo.add(aluno)

    def __str__(self):
        return f"Relatório do Professor {self.professor.usuario.username} - Disciplina {self.disciplina}"

class NotaRelatorio(models.Model):
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.FloatField(null=True, default=0)

    def __str__(self):
        return f"NotaRelatorio: {self.aluno.usuario.username} - Nota: {self.nota}"

class FaltaRelatorio(models.Model):
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    faltas = models.IntegerField(default=0)

    def __str__(self):
        return f"FaltaRelatorio: {self.aluno.usuario.username} - Faltas: {self.faltas}"