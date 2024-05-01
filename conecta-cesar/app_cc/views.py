from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Disciplina, Nota, Diario, Professor as ProfessorModel, Aluno as AlunoModel, Falta
from rolepermissions.checkers import has_role
from project_cc.roles import Professor, Aluno
from django.contrib import messages
from datetime import date
from functools import wraps

def has_role_or_redirect(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verificar se o usuário está autenticado
            if not request.user.is_authenticated:
                messages.error(request, "Você precisa fazer login para acessar esta página.")
                return redirect(reverse("login"))  # Redireciona para a página de login
            
            # Verificar se o usuário é administrador (superuser)
            if request.user.is_superuser:
                messages.error(request, "Administradores não têm acesso a esta página.")
                return redirect(reverse("login"))  # Redireciona para a página de login com mensagem de erro
            
            # Verificar se o usuário tem o papel necessário
            if not has_role(request.user, required_role):
                messages.error(request, f"Permissão negada. Você precisa ser '{required_role.__name__}' para acessar esta página.")
                return redirect(reverse("login"))  # Redireciona para a página de login com mensagem de erro
            
            # Se o usuário está autenticado e tem o papel correto, permite o acesso à view
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator
# -----------------STUDENT VIEWS--------------------------------------------
@has_role_or_redirect(Aluno)
def avisos(request):
    return render(request, 'app_cc/aluno/avisos.html')

#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Aluno)
def disciplinas_e_notas(request):
    disciplinas_com_notas = []
    disciplinas = Disciplina.objects.all()
    for disciplina in disciplinas:
        notas = Nota.objects.filter(disciplina=disciplina)
        disciplinas_com_notas.append((disciplina, notas))
    return render(request, 'app_cc/aluno/disciplina.html', {'disciplinas_com_notas': disciplinas_com_notas})

#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Aluno)
def boletim(request):
    # Obter o aluno associado ao usuário autenticado
    aluno = AlunoModel.objects.get(usuario=request.user)

    # Obter todas as disciplinas associadas à turma do aluno
    disciplinas = aluno.turma.disciplinas.all()

    # Crie uma lista para armazenar as disciplinas e suas notas
    disciplinas_com_notas = []

    for disciplina in disciplinas:
        # Tentar obter a nota para a disciplina
        try:
            nota_instance = Nota.objects.get(disciplina=disciplina, aluno=aluno)
        except Nota.DoesNotExist:
            nota_instance = None

        # Adicionar disciplina e nota à lista
        disciplinas_com_notas.append((disciplina.nome, nota_instance))

    # Renderize o template com as disciplinas e notas associadas
    return render(request, 'app_cc/aluno/boletim.html', {'disciplinas_com_notas': disciplinas_com_notas})
#----------------------------------------------------------------------------------------------------------------   
@has_role_or_redirect(Aluno) 
def frequencia(request):
    # Obter o aluno atual
    aluno = request.user.aluno

    # Obter disciplinas associadas à turma do aluno
    disciplinas = aluno.turma.disciplinas.all()

    disciplinas_com_faltas = []

    # Para cada disciplina, conte as faltas do aluno
    for disciplina in disciplinas:
        # Encontrar todas as faltas para esta disciplina
        faltas = Falta.objects.filter(aluno=aluno).count()

        # Supondo que cada disciplina tenha um número fixo de aulas no semestre
        total_de_aulas = 15  # Defina o número total de aulas para a disciplina
        frequencia = 100 * (1 - (faltas / total_de_aulas))  # Calcular a frequência percentual

        disciplinas_com_faltas.append({
            'disciplina': disciplina,
            'faltas': faltas,
            'frequencia': frequencia
        })

    return render(
        request,
        'app_cc/aluno/frequencia.html',
        {'disciplinas_com_faltas': disciplinas_com_faltas}
    )
#---------------------------------------------------------------------------------------------------------------- 
   
@has_role_or_redirect(Aluno)
def perfil(request):
    try:
        # Tenta obter o professor associado ao usuário logado
        aluno = AlunoModel.objects.get(usuario=request.user)
        context = {
            'nome': aluno.usuario.username,
            'email': aluno.email,
            'ra':aluno.ra
        }
    except ProfessorModel.DoesNotExist:
        # Se o professor não existir, exibe uma mensagem ou redireciona
        messages.error(request, "Aluno associado não encontrado.")
        return redirect("login")  # Redirecionar para uma página de erro ou uma página apropriada

    return render(request, 'app_cc/aluno/perfil.html', context)

#---------------------------------------------------------------------------------------------------------------- 

@has_role_or_redirect(Aluno)
def diario(request):
    # Obtém todos os diários salvos
    diarios = Diario.objects.all()
    # Renderiza o template 'app_cc/diario.html' passando os diários para o contexto
    return render(request, 'app_cc/aluno/diario.html', {'diarios': diarios})


@has_role_or_redirect(Aluno)
def calendario(request):
    return render('app_cc/aluno/calendario.html')

#----------------------------------------------------------------------------------------------------------------    
#----------------------------------------PROFESSOR VIEWS---------------------------------------------------------  
#----------------------------------------------------------------------------------------------------------------    

@has_role_or_redirect(Professor)
def turmas(request):
    return render(request, 'app_cc/professor/turmas.html')
#----------------------------------------------------------------------------------------------------------------    

@has_role_or_redirect(Professor)
def perfilp(request):
    try:
        # Tenta obter o professor associado ao usuário logado
        professor = ProfessorModel.objects.get(usuario=request.user)
        context = {
            'nome': professor.usuario.username,
            'email': professor.email,
            'ra':professor.ra
        }
    except ProfessorModel.DoesNotExist:
        # Se o professor não existir, exibe uma mensagem ou redireciona
        messages.error(request, "Professor associado não encontrado.")
        return redirect("login")  # Redirecionar para uma página de erro ou uma página apropriada

    return render(request, 'app_cc/professor/perfilp.html', context)
#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Professor)
def frequenciap(request):
    professor = request.user.professor
    disciplinas = Disciplina.objects.filter(professor=professor)
    hoje = date.today()

    if request.method == "POST":
        # Colete todas as faltas que deveriam existir após o POST
        faltas_depois_do_post = set(request.POST.keys())
        
        # Para cada disciplina, turma e aluno, verifique se a falta deve ser adicionada ou removida
        for disciplina in disciplinas:
            for turma in disciplina.turmas.all():
                for aluno in AlunoModel.objects.filter(turma=turma):
                    falta_key = f"falta[{aluno.id}]"

                    # Se o checkbox está marcado, adicionar a falta
                    if falta_key in faltas_depois_do_post:
                        if not Falta.objects.filter(aluno=aluno, data=hoje).exists():
                            Falta.objects.create(aluno=aluno, data=hoje)
                    # Se o checkbox está desmarcado, remover a falta se ela existir
                    else:
                        Falta.objects.filter(aluno=aluno, data=hoje).delete()

    # Estrutura para disciplinas, turmas e alunos, com totais de faltas
    disciplinas_com_turmas_e_alunos = []
    for disciplina in disciplinas:
        disciplina_info = {
            'disciplina': disciplina,
            'turmas': []
        }

        for turma in disciplina.turmas.all():
            alunos_na_turma = AlunoModel.objects.filter(turma=turma)
            turma_info = {
                'turma': turma,
                'alunos': []
            }

            for aluno in alunos_na_turma:
                total_faltas = Falta.objects.filter(aluno=aluno).count()
                tem_falta_hoje = Falta.objects.filter(aluno=aluno, data=hoje).exists()
                aluno_info = {
                    'aluno': aluno,
                    'turma': turma,
                    'total_faltas': total_faltas,
                    'tem_falta_hoje': tem_falta_hoje
                }
                turma_info['alunos'].append(aluno_info)

            disciplina_info['turmas'].append(turma_info)

        disciplinas_com_turmas_e_alunos.append(disciplina_info)

    # Renderizar o template com as disciplinas, turmas e alunos
    return render(
        request,
        'app_cc/professor/frequenciap.html',
        {'disciplinas_com_turmas_e_alunos': disciplinas_com_turmas_e_alunos}
    )
#----------------------------------------------------------------------------------------------------------------    

@has_role_or_redirect(Professor)
def calendariop(request):
    return render(request, 'app_cc/professor/calendariop.html')
#----------------------------------------------------------------------------------------------------------------    

@has_role_or_redirect(Professor)
def diariop(request):
    if request.method == 'POST':
        disciplina = request.POST.get('disciplina')
        titulo = request.POST.get('titulo')
        texto = request.POST.get('texto')
        Diario.objects.create(disciplina=disciplina, titulo=titulo, texto=texto)
        return redirect('diariop')
    else:
        diarios = Diario.objects.all()
        return render(request, 'app_cc/professor/diariop.html', {'diarios': diarios})
#----------------------------------------------------------------------------------------------------------------    

@has_role_or_redirect(Professor)
def avisosp(request):
    return render(request, 'app_cc/professor/avisosp.html')
#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Professor)
def boletimp(request):
    disciplinas = Disciplina.objects.filter(professor__usuario=request.user)
    if request.method == "POST":
        for disciplina in disciplinas:
            turmas = disciplina.turmas.all()
            for turma in turmas:
                for aluno in AlunoModel.objects.filter(turma=turma):
                    nota_key = f"notas[{aluno.usuario.username}-{turma.id}]"
                    nota_value = request.POST.get(nota_key)

                    if nota_value:
                        try:
                            nota_float = float(nota_value.replace(',', '.'))
                            if nota_float < 0 or nota_float > 10:
                                messages.error(request, "A nota deve estar entre 0 e 10.")
                                return redirect("boletimp")

                            nota, created = Nota.objects.get_or_create(
                                disciplina=disciplina,
                                aluno=aluno
                            )
                            nota.valor = nota_float
                            nota.save()

                        except ValueError:
                            messages.error(request, "Valor inválido para nota.")
                            return redirect("boletimp")

    # Aqui, criamos uma estrutura que inclui as notas associadas a cada aluno
    disciplinas_com_turmas_e_alunos = []
    for disciplina in disciplinas:
        disciplina_info = {
            'disciplina': disciplina,
            'turmas': disciplina.turmas.all(),
            'alunos_com_notas': []  # Lista para armazenar alunos e suas notas
        }

        for turma in disciplina_info['turmas']:
            alunos_na_turma = AlunoModel.objects.filter(turma=turma)
            for aluno in alunos_na_turma:
                nota = Nota.objects.filter(disciplina=disciplina, aluno=aluno).first()  # Nota associada
                nota_valor = nota.valor if nota else 0  # Se não houver nota, usar 0
                disciplina_info['alunos_com_notas'].append({
                    'aluno': aluno,
                    'turma': turma,
                    'nota': nota_valor
                })

        disciplinas_com_turmas_e_alunos.append(disciplina_info)

    return render(
        request,
        'app_cc/professor/boletimp.html',
        {'disciplinas_com_turmas_e_alunos': disciplinas_com_turmas_e_alunos}
    )