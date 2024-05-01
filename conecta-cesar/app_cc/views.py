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
    try:
        # Obter o aluno associado ao usuário autenticado
        aluno = AlunoModel.objects.get(usuario=request.user)
    except AlunoModel.DoesNotExist:
        aluno = None

    if aluno and aluno.turma:
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

        context = {
            'disciplinas_com_notas': disciplinas_com_notas
        }
    else:
        context = {
            'error': 'Turma ou disciplinas não encontradas para o aluno.'  # Caso de erro
        }

    return render(request, 'app_cc/aluno/boletim.html', context)
#----------------------------------------------------------------------------------------------------------------   
@has_role_or_redirect(Aluno) 
def frequencia(request):
    try:
        # Obter o aluno associado ao usuário autenticado
        aluno = request.user.aluno
    except AlunoModel.DoesNotExist:
        aluno = None

    disciplinas_com_faltas = []

    if aluno and aluno.turma:
        # Obter disciplinas associadas à turma do aluno
        disciplinas = aluno.turma.disciplinas.all()

        for disciplina in disciplinas:
            # Encontrar todas as faltas do aluno para essa disciplina específica
            faltas = Falta.objects.filter(aluno=aluno, disciplina=disciplina).count()

            # Supondo um número fixo de aulas por disciplina
            total_de_aulas = 15  # Valor ajustável
            frequencia = 100 * (1 - (faltas / total_de_aulas))  # Calcular a frequência

            disciplinas_com_faltas.append({
                'disciplina': disciplina,
                'faltas': faltas,
                'frequencia': frequencia
            })

        context = {
            'disciplinas_com_faltas': disciplinas_com_faltas
        }
    else:
        context = {
            'error': 'Nenhuma disciplina ou turma encontrada para o aluno.'
        }

    return render(request, 'app_cc/aluno/frequencia.html', context)
#---------------------------------------------------------------------------------------------------------------- 
   

@has_role_or_redirect(Aluno) 
def variacao_notas(request):
    try:
        aluno = AlunoModel.objects.get(usuario=request.user)
    except AlunoModel.DoesNotExist:
        aluno = None

    disciplinas_com_notas = []

    if aluno and aluno.turma:
        disciplinas = aluno.turma.disciplinas.all()

        for disciplina in disciplinas:
            nota_instance = Nota.objects.filter(aluno=aluno, disciplina=disciplina).first()
            nota = nota_instance.valor if nota_instance else 0

            # Calcular a largura das barras
            largura = max(nota * 10, 2)  # Largura mínima de 2% para notas zero

            disciplinas_com_notas.append({
                'disciplina': disciplina.nome,
                'nota': nota,
                'largura': largura
            })

    return render(request, 'app_cc/aluno/variacao_notas.html', {
        'disciplinas_com_notas': disciplinas_com_notas
    })
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
    try:
        # Obter o aluno associado ao usuário autenticado
        aluno = AlunoModel.objects.get(usuario=request.user)
    except AlunoModel.DoesNotExist:
        aluno = None

    if aluno and aluno.turma:
        # Obter disciplinas associadas à turma do aluno
        disciplinas = aluno.turma.disciplinas.all()

        # Obter diários associados às disciplinas do aluno
        diarios = Diario.objects.filter(disciplina__in=disciplinas)

        context = {
            'diarios': diarios,
            'disciplinas': disciplinas
        }
    else:
        context = {
            'error': 'Turma não encontrada ou sem disciplinas associadas.'  # Caso de erro
        }

    return render(request, 'app_cc/aluno/diario.html', context)


@has_role_or_redirect(Aluno)
def calendario(request):
    return render(request, 'app_cc/aluno/calendario.html')

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
        faltas_depois_do_post = set(request.POST.keys())

        # Processar faltas para cada disciplina individualmente
        for disciplina in disciplinas:
            for turma in disciplina.turmas.all():
                for aluno in AlunoModel.objects.filter(turma=turma):
                    falta_key = f"falta[{aluno.id}-{disciplina.id}]"

                    # Adicionar falta para a disciplina correta
                    if falta_key in faltas_depois_do_post:
                        if not Falta.objects.filter(aluno=aluno, data=hoje, disciplina=disciplina).exists():
                            Falta.objects.create(aluno=aluno, data=hoje, disciplina=disciplina)

                    # Remover falta para a disciplina correta
                    else:
                        Falta.objects.filter(aluno=aluno, data=hoje, disciplina=disciplina).delete()

    # Estrutura para disciplinas, turmas e alunos, com totais de faltas
    disciplinas_com_turmas_e_alunos = []

    for disciplina in disciplinas:
        disciplina_info = {
            'disciplina': disciplina,
            'turmas': []
        }

        for turma in disciplina.turmas.all():
            turma_info = {
                'turma': turma,
                'alunos': []
            }

            for aluno in AlunoModel.objects.filter(turma=turma):
                total_faltas = Falta.objects.filter(aluno=aluno, disciplina=disciplina).count()
                tem_falta_hoje = Falta.objects.filter(aluno=aluno, data=hoje, disciplina=disciplina).exists()
                
                aluno_info = {
                    'aluno': aluno,
                    'total_faltas': total_faltas,
                    'tem_falta_hoje': tem_falta_hoje
                }

                turma_info['alunos'].append(aluno_info)

            disciplina_info['turmas'].append(turma_info)

        disciplinas_com_turmas_e_alunos.append(disciplina_info)

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
    professor = request.user.professor  # Obter o professor associado ao usuário

    # Obter todas as disciplinas associadas ao professor
    disciplinas = Disciplina.objects.filter(professor=professor)

    if request.method == 'POST':
        # Obter dados do POST
        disciplina_id = request.POST.get('disciplina')
        titulo = request.POST.get('titulo')
        texto = request.POST.get('texto')

        # Verificar se a disciplina pertence ao professor
        disciplina = Disciplina.objects.filter(id=disciplina_id, professor=professor).first()

        if disciplina:
            # Criar um novo diário para essa disciplina
            Diario.objects.create(disciplina=disciplina, titulo=titulo, texto=texto)
            return redirect('diariop')  # Redirecionar para a mesma página
        else:
            return messages.error(request, "Disciplina não permitida.")  # Caso de erro

    else:
        # Obter todos os diários associados às disciplinas do professor
        diarios = Diario.objects.filter(disciplina__in=disciplinas)

        context = {
            'disciplinas': disciplinas,
            'diarios': diarios
        }

        return render(request, 'app_cc/professor/diariop.html', context)
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
            for turma in disciplina.turmas.all():
                for aluno in AlunoModel.objects.filter(turma=turma):
                    # Cria a chave de nota única para cada aluno-disciplina-turma
                    nota_key = f"notas[{aluno.usuario.username}-{turma.id}-{disciplina.id}]"
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

    # Estrutura para disciplinas, turmas e alunos, com notas
    disciplinas_com_turmas_e_alunos = []

    for disciplina in disciplinas:
        disciplina_info = {
            'disciplina': disciplina,
            'turmas': disciplina.turmas.all(),
            'alunos_com_notas': []
        }

        for turma in disciplina_info['turmas']:
            alunos_na_turma = AlunoModel.objects.filter(turma=turma)
            for aluno in alunos_na_turma:
                nota = Nota.objects.filter(disciplina=disciplina, aluno=aluno).first()
                nota_valor = nota.valor if nota else 0

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