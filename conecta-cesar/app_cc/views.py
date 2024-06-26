from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Like, Post, Review, Disciplina, Nota, Diario, Professor as ProfessorModel, Aluno as AlunoModel, Falta, File, Evento, Aviso, Relatorio, ProfessorFile, Turma, Atividade, AtividadeFeita
from rolepermissions.checkers import has_role
from project_cc.roles import Professor, Aluno
from django.contrib import messages
from datetime import date
from functools import wraps
from django.conf import settings
import os
import json
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
from .models import ToDoItem, ToDoList
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import Http404



def gerar_relatorio(disciplinas, professor):
    for disciplina in disciplinas:
        try:
            # Tenta obter um relatório existente para o professor e a disciplina
            relatorio = Relatorio.objects.get(professor=professor, disciplina=disciplina)
            print("Relatório existente encontrado:", relatorio)
            relatorio.delete()
            print("Relatório existente excluído.")

        except ObjectDoesNotExist:
            pass
        relatorio = Relatorio.objects.create(professor=professor, disciplina=disciplina)
        print("Novo relatório criado:", relatorio)
        relatorio.atualizar_relatorio(disciplina)

def gerar_sigla(nome):
            # Divide por espaços e pega a primeira letra de cada palavra
            return "".join([palavra[0].upper() for palavra in nome.split()])

def has_role_or_redirect(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verificar se o usuário está autenticado
            if not request.user.is_authenticated:
                messages.error(request, _("Você precisa fazer login para acessar esta página."))
                return redirect(reverse("login"))  # Redireciona para a página de login
            
            # Verificar se o usuário é administrador (superuser)
            if request.user.is_superuser:
                messages.error(request, _("Administradores não têm acesso a esta página."))
                return redirect(reverse("login"))  # Redireciona para a página de login com mensagem de erro
            
            # Verificar se o usuário tem o papel necessário
            if not has_role(request.user, required_role):
                messages.error(request, _(f"Permissão negada. Você precisa ser '{required_role.__name__}' para acessar esta página."))
                return redirect(reverse("login"))  # Redireciona para a página de login com mensagem de erro
            
            # Se o usuário está autenticado e tem o papel correto, permite o acesso à view
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator
# -----------------STUDENT VIEWS--------------------------------------------
@has_role_or_redirect(Aluno)
def avisos(request):
    avisos=Aviso.objects.all()
    return render(request, 'app_cc/aluno/avisos.html', {'avisos':avisos})

@has_role_or_redirect(Aluno)
def detalhe_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, pk=aviso_id)
    return render(request, 'app_cc/aluno/detalhe_aviso.html', {'aviso': aviso})

#----------------------------------------------------------------------------------------------------------------  
@has_role_or_redirect(Aluno)
def hora_extra(request):
    # Obter o aluno associado ao usuário autenticado
    aluno = AlunoModel.objects.get(usuario=request.user)

    if request.method == "GET":
        # Obter os arquivos enviados pelo aluno
        arquivos = File.objects.filter(aluno=aluno)

        # Calcular o total de horas extras acumuladas
        total_horas_extras = sum([arquivo.horas_extras for arquivo in arquivos])

        return render(
            request,
            "app_cc/aluno/hora_extra.html",
            {"arquivos": arquivos, "total_horas_extras": total_horas_extras},
        )

    elif request.method == "POST":
        # Se for exclusão de arquivo
        if "delete_file" in request.POST:
            file_id = request.POST.get("delete_file")
            try:
                file = File.objects.get(id=file_id, aluno=aluno)

                # Deletar do sistema de arquivos e banco de dados
                if os.path.exists(file.archive.path):
                    os.remove(file.archive.path)
                file.delete()
                messages.success(request, _("Arquivo excluído com sucesso."))
            except File.DoesNotExist:
                messages.error(request, _("Arquivo não encontrado para exclusão."))

            return redirect("hora_extra")

        # Para atualização de horas extras
        elif "update_file" in request.POST:
            file_id = request.POST.get("update_file")
            horas_extras = request.POST.get("horas_extras")

            # Verificar se o campo está vazio
            if not horas_extras or horas_extras.strip() == "":
                messages.error(request, _("O campo de horas extras não pode ser vazio."))
                return redirect("hora_extra")

            try:
                horas_extras = float(horas_extras)
                if horas_extras <= 0:
                    messages.error(request, "Horas extras devem ser maior que 0.")
                    return redirect("hora_extra")
            except ValueError:
                messages.error(_("Valor inválido para horas extras."))
                return redirect("hora_extra")

            try:
                file = File.objects.get(id=file_id, aluno=aluno)
                file.horas_extras = horas_extras
                file.save()
                messages.success(request, _("Horas extras atualizadas com sucesso."))
            except File.DoesNotExist:
                messages.error(request, _("Arquivo não encontrado para atualização."))

            return redirect("hora_extra")

        # Para uploads de novos arquivos
        file = request.FILES.get("my_file")
        horas_extras = request.POST.get("horas_extras")

        if not file:
            messages.error(_("Nenhum arquivo recebido."))
            return redirect("hora_extra")

        # Verificar se o tipo do arquivo é aceitável
        if not file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            messages.error(request, _("Somente arquivos JPG ou PNG são permitidos."))
            return redirect("hora_extra")

        if not horas_extras or horas_extras.strip() == "":
            messages.error(request, _("O campo de horas extras não pode ser vazio."))
            return redirect("hora_extra")

        try:
            horas_extras = float(horas_extras)
            if horas_extras <= 0:
                messages.error(request, _("Horas extras devem ser maior que 0."))
                return redirect("hora_extra")
        except ValueError:
            messages.error(request, _("Valor inválido para horas extras."))
            return redirect("hora_extra")

        # Se for um novo arquivo
        file_name_with_date = f"{file.name[:-4]}-{date.today()}.jpg"
        
        file_path = os.path.join(settings.MEDIA_ROOT, f"user_files/{file_name_with_date}")

        # Salvar o arquivo diretamente no sistema de arquivos
        with open(file_path, "wb+") as destino:
            for chunk in file.chunks():
                destino.write(chunk)

        # Criar um objeto do modelo `File`
        archive = File(
            title=file_name_with_date,
            archive=f"user_files/{file_name_with_date}",
            aluno=aluno,
            horas_extras=horas_extras,
        )
        archive.save()

        messages.success(request, _("Arquivo salvo com sucesso."))
        return redirect("hora_extra")
   
#----------------------------------------------------------------------------------------------------------------    



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
            'error': _('Turma ou disciplinas não encontradas para o aluno.')  # Caso de erro
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
            'error': _('Nenhuma disciplina ou turma encontrada para o aluno.')
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

            largura = max((nota / 10) * 100, 2)  # Calcular largura das barras no back-end

            disciplinas_com_notas.append({
                'disciplina': gerar_sigla(disciplina.nome),  # Obter sigla
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
        aluno = AlunoModel.objects.get(usuario=request.user)
        
        if request.method == 'POST':
            foto_perfil = request.FILES.get('foto_perfil')  # Captura o arquivo enviado pelo formulário

            if foto_perfil:
                # Verifique se o arquivo é PNG ou JPG
                ext = os.path.splitext(foto_perfil.name)[1].lower()  # Pega a extensão do arquivo
                if ext not in ['.jpg', '.jpeg', '.png']:
                    messages.error(request, _("Somente arquivos JPG ou PNG são permitidos."))
                    return redirect('perfil')  # Redireciona para a mesma página

                # Se há uma foto antiga, exclua-a
                if aluno.foto_perfil and os.path.isfile(aluno.foto_perfil.path):
                    os.remove(aluno.foto_perfil.path)

                # Atribua a nova foto de perfil ao modelo
                aluno.foto_perfil = foto_perfil
                aluno.save()
                messages.success(request, _("Foto de perfil atualizada com sucesso!"))
            else:
                messages.error(request, _("Por favor, envie uma nova foto de perfil."))

        context = {
            'nome': aluno.usuario.username,
            'email': aluno.email,
            'ra': aluno.ra,
            'foto_perfil': aluno.foto_perfil.url if aluno.foto_perfil else None,
        }

    except AlunoModel.DoesNotExist:
        messages.error(request, _("Aluno associado ao usuário não encontrado."))
        return redirect("login")

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
            'error': _('Turma não encontrada ou sem disciplinas associadas.')  # Caso de erro
        }

    return render(request, 'app_cc/aluno/diario.html', context)


@has_role_or_redirect(Aluno)
def calendario(request):
    # Obtém o aluno logado
    aluno = request.user.aluno

    # Obtém todas as disciplinas associadas à turma do aluno
    disciplinas = aluno.turma.disciplinas.all()

    # Obtém todos os eventos que estão associados a alguma dessas disciplinas
    eventos = Evento.objects.filter(disciplina__in=disciplinas)
    print(eventos)

    # Converte os eventos em uma lista de dicionários, contendo apenas os campos
    # 'titulo', 'descricao', 'data', 'horario' e 'disciplina__nome'
    eventos_list = list(eventos.values('titulo', 'descricao', 'data', 'horario', 'disciplina__nome'))
    # Serializa a lista de dicionários em formato JSON
    eventos_json = json.dumps(eventos_list, default=str)

    # Cria um dicionário com a chave 'eventos_json' e o valor correspondente
    context = {
        'eventos_json': eventos_json,
        'eventos': eventos
    }
    print(context)

    return render(request, 'app_cc/aluno/calendario.html', context)

#----------------------------------------------------------------------------------------------------------------    
#----------------------------------------PROFESSOR VIEWS---------------------------------------------------------  
#---------------------------------------------------------------------------------------------------------------- 

@has_role_or_redirect(Aluno)
def slides(request):
    aluno=AlunoModel.objects.get(usuario=request.user)
    disciplinas=Turma.obter_disciplinas(aluno.turma)
    print(disciplinas)
    arquivos=ProfessorFile.objects.filter(disciplina__in=disciplinas)

    print(arquivos)

    return render(request, "app_cc/aluno/slides.html", {"arquivos": arquivos, "disciplinas": disciplinas})

@has_role_or_redirect(Professor)
def slidesp(request):
    # Obter o professor associado ao usuário autenticado
    professor = ProfessorModel.objects.get(usuario=request.user)
    disciplinas=Disciplina.objects.filter(professor=professor)



    if request.method == "GET":
        # Obter os arquivos enviados pelo professor
        arquivos = ProfessorFile.objects.filter(professor=professor)

        return render(
            request,
            "app_cc/professor/slidesp.html",
            {"arquivos": arquivos, "disciplinas": disciplinas},
        )

    elif request.method == "POST":
        # Se for exclusão de arquivo
        if "delete_file" in request.POST:
            file_id = request.POST.get("delete_file")
            try:
                file = ProfessorFile.objects.get(id=file_id, professor=professor)

                # Deletar do sistema de arquivos e banco de dados
                if file.archive:
                    if os.path.exists(file.archive.path):
                        os.remove(file.archive.path)
                file.delete()
                messages.success(request, _("Arquivo excluído com sucesso."))
            except ProfessorFile.DoesNotExist:
                messages.error(request, _("Arquivo não encontrado para exclusão."))

            return redirect("slidesp")

        # Para atualização de horas extras
        
        # Para uploads de novos arquivos
        file = request.FILES.get("slide_file")
        titulo = request.POST.get("slide_titulo")
        descricao = request.POST.get("slide_descricao")
        disciplina = request.POST.get("slide_disciplina")

        disciplina=Disciplina.objects.get(nome=disciplina)

        # Verificar se o tipo do arquivo é aceitável
        if file:
            ext_permitidas = ('.jpg', '.jpeg', '.png', '.pdf', '.pptx', '.docx')
            if not file.name.lower().endswith(ext_permitidas):
                messages.error(request, _("Tipo de arquivo não permitido."))
                return redirect("slidesp")

            ext = file.name.split('.')[-1]

            # Se for um novo arquivo
            file_name_with_date = f"{file.name.rsplit('.', 1)[0]}-{date.today()}.{ext}"

            file_path = os.path.join(settings.MEDIA_ROOT, f"documentosp/{file_name_with_date}")

            # Salvar o arquivo diretamente no sistema de arquivos
            with open(file_path, "wb+") as destino:
                for chunk in file.chunks():
                    destino.write(chunk)

            # Criar um objeto do modelo `ProfessorFile`
            archive = ProfessorFile(
                titulo=titulo,
                descricao=descricao,
                archive=f"documentosp/{file_name_with_date}",
                professor=professor,
                disciplina=disciplina,
            )
            print(archive)
            archive.save()
        else:
            archive = ProfessorFile(
                titulo=titulo,
                descricao=descricao,
                professor=professor,
                disciplina=disciplina,
            )
            archive.save()
            print(archive)

        messages.success(request, _("Documento salvo com sucesso."))
        return redirect("slidesp")
    
    # Após lidar com POST, renderizar com 'ext' no contexto
    arquivos = ProfessorFile.objects.filter(professor=professor)
    return render(
        request,
        "app_cc/professor/slidesp.html",
        {"arquivos": arquivos, },
    )

#----------------------------------------------------------------------------------------------------------------    

@has_role_or_redirect(Professor)  # Garante que apenas usuários com papel de professor têm acesso
def perfilp(request):
    try:
        professor = ProfessorModel.objects.get(usuario=request.user)
        
        if request.method == 'POST':
            foto_perfil = request.FILES.get('foto_perfil')  # Captura o arquivo enviado pelo formulário

            if foto_perfil:
                # Verifica se o arquivo é do tipo correto (PNG ou JPG)
                extensao = os.path.splitext(foto_perfil.name)[1].lower()  # Obtém a extensão do arquivo
                if extensao not in ['.jpg', '.jpeg', '.png']:  # Checa se é um formato válido
                    messages.error(request, _("Somente arquivos JPG ou PNG são permitidos."))
                    return redirect("perfilp")  # Redireciona para a mesma página

                # Se existe uma foto anterior, remova-a
                if professor.foto_perfil and os.path.isfile(professor.foto_perfil.path):
                    os.remove(professor.foto_perfil.path)

                # Atribua a nova foto de perfil ao modelo
                professor.foto_perfil = foto_perfil
                professor.save()
                messages.success(request, _("Foto de perfil atualizada com sucesso!"))
            else:
                messages.error(request, _("Por favor, envie uma nova foto de perfil."))

        context = {
            'nome': professor.usuario.username,
            'email': professor.email,
            'ra': professor.ra,
            'foto_perfil': professor.foto_perfil.url if professor.foto_perfil else None,
        }

    except ProfessorModel.DoesNotExist:
        messages.error(request, _("Professor associado ao usuário não encontrado."))
        return redirect("login")

    return render(request, 'app_cc/professor/perfilp.html', context)
#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Professor)
def frequenciap(request):
    professor = ProfessorModel.objects.get(usuario=request.user)
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

        gerar_relatorio(disciplinas, professor)

    return render(
        request,
        'app_cc/professor/frequenciap.html',
        {'disciplinas_com_turmas_e_alunos': disciplinas_com_turmas_e_alunos}
    )
#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Professor)
def relatoriop(request):
    professor = ProfessorModel.objects.get(usuario=request.user)
    relatorios=Relatorio.objects.filter(professor=professor)
    disciplinas=Disciplina.objects.filter(professor=professor)
    gerar_relatorio(disciplinas, professor)
    print(relatorios)
    return render(request, "app_cc/professor/relatoriosp.html", {"relatorios":relatorios,})

#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Professor)
def calendariop(request):
    professor = ProfessorModel.objects.get(usuario=request.user)
    disciplinas = Disciplina.objects.filter(professor=professor)

    if request.method == "POST":  # Corrigido para 'POST'
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        disciplina_id = request.POST.get('disciplina')

        try:
            disciplina = Disciplina.objects.get(id=disciplina_id)
            Evento.objects.create(
                titulo=titulo,
                descricao=descricao,
                data=data,
                horario=horario,
                disciplina=disciplina,
                professor=professor  # Usar a instância do professor corretamente
            )
            messages.success(request, _('Evento criado com sucesso!'))
        except Disciplina.DoesNotExist:
            messages.error(request, _('Disciplina não encontrada.'))
        except Exception as e:
            messages.error(request, f'Erro ao criar evento: {str(e)}')

        return redirect('calendariop')
    
    else:
        eventos = Evento.objects.filter(professor=professor)
        eventos_list = list(eventos.values('titulo', 'descricao', 'data', 'horario', 'disciplina__nome'))
        eventos_json = json.dumps(eventos_list, default=str)  # Serializar para JSON
        context = {
            'disciplinas': disciplinas,
            'eventos_json': eventos_json ,              # Passando os eventos serializados
            'eventos': eventos,
        }
        return render(request, 'app_cc/professor/calendariop.html', context)
    
#----------------------------------------------------------------------------------------------------------------    

@has_role_or_redirect(Professor)
def diariop(request):
    professor = ProfessorModel.objects.get(usuario=request.user)
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
            return messages.error(request, _("Disciplina não permitida."))  # Caso de erro

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
    avisos=Aviso.objects.all()
    return render(request, 'app_cc/professor/avisosp.html', {"avisos":avisos})

@has_role_or_redirect(Professor)
def detalhe_avisop(request, aviso_id):
    aviso = get_object_or_404(Aviso, pk=aviso_id)
    return render(request, 'app_cc/professor/detalhe_avisop.html', {'aviso': aviso})
#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Professor)
def boletimp(request):
    
    alunos = AlunoModel.objects.all()  
    alunos_notas = []
    for aluno in alunos:
        notas = aluno.notas.all()
        alunos_notas.extend(notas)
    print(alunos_notas)


    # Obtém o objeto ProfessorModel do usuário logado
    professor = ProfessorModel.objects.get(usuario=request.user)
    # Obter todas as disciplinas associadas ao professor
    disciplinas = Disciplina.objects.filter(professor=professor)
    
    if request.method == "POST":
        # Percorre cada disciplina, turma e aluno
        for disciplina in disciplinas:
            for turma in disciplina.turmas.all():
                for aluno in AlunoModel.objects.filter(turma=turma):
                    # Cria a chave de nota única para cada aluno-disciplina-turma
                    nota_key = f"notas[{aluno.usuario.username}-{turma.id}-{disciplina.id}]"
                    # Obtém o valor da nota do POST
                    nota_value = request.POST.get(nota_key)

                    if nota_value:
                        try:
                            # Converte a nota para float e verifica se está dentro do intervalo permitido
                            nota_float = float(nota_value.replace(',', '.'))
                            if nota_float < 0 or nota_float > 10:
                                messages.error(request, _("A nota deve estar entre 0 e 10."))
                                return redirect("boletimp")

                            # Cria ou atualiza a nota do aluno
                            nota, created = Nota.objects.get_or_create(
                                disciplina=disciplina,
                                aluno=aluno
                            )
                            nota.valor = nota_float
                            nota.save()
                            # Gera o relatório
                            gerar_relatorio(disciplinas, professor)

                        except ValueError:
                            # Caso a nota seja inválida, exibe uma mensagem de erro
                            messages.error(request, _("Valor inválido para nota."))
                            return redirect("boletimp")

    # Cria uma estrutura para armazenar as disciplinas, turmas e alunos com suas notas
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
                # Obtém a nota do aluno para a disciplina
                nota = Nota.objects.filter(disciplina=disciplina, aluno=aluno).first()
                nota_valor = nota.valor if nota else 0

                disciplina_info['alunos_com_notas'].append({
                    'aluno': aluno,
                    'turma': turma,
                    'nota': nota_valor,
                    
                })

        disciplinas_com_turmas_e_alunos.append(disciplina_info)

    # Renderiza a página com a estrutura de disciplinas, turmas e alunos, com suas notas
    return render(
        request,
        'app_cc/professor/boletimp.html',
        {'disciplinas_com_turmas_e_alunos': disciplinas_com_turmas_e_alunos}
    )

@login_required
def todo_list_view(request):
    user = request.user
    todo_lists = ToDoList.objects.filter(user=user)
    return render(request, 'app_cc/aluno/todo_list.html', {'todo_lists': todo_lists})

@login_required
def create_todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()  # Obtém o título do POST e remove espaços em branco extras
        if title:
            ToDoList.objects.create(user=request.user, title=title)
            return redirect('todo_list')  # Redireciona para a lista de tarefas após a criação
        else:
            # Caso o título esteja vazio, pode adicionar lógica para lidar com o erro ou retornar ao formulário
            return render(request, 'app_cc/aluno/create_todo_list.html', {'error_message': 'Por favor, preencha o título.'})
    else:
        return render(request, 'app_cc/aluno/create_todo_list.html')


@login_required
def add_todo_item(request, list_id):
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        priority = request.POST.get('priority')
        
        ToDoItem.objects.create(todo_list=todo_list, content=content, priority=priority)
        return redirect('todo_list')
           
    return render(request, 'app_cc/aluno/add_todo_item.html', {'todo_list': todo_list})

@login_required
def delete_todo_list(request, list_id):
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    todo_list.delete()
    return redirect('todo_list')

@login_required
def delete_todo_item(request, item_id):
    item = get_object_or_404(ToDoItem, id=item_id, todo_list__user=request.user)
    item.delete()
    return redirect('todo_list')
    


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@login_required
def forum_view(request):
    posts = Post.objects.all()
    return render(request, 'app_cc/aluno/forum.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        corpo = request.POST.get('corpo')
        autor_id = request.user.id  # Assume que o usuário está autenticado
        publicado_em = timezone.now()
        pdf = request.FILES.get('pdf')  # Assume que o formulário tem um campo de upload de arquivo para o pdf

        if titulo and corpo and autor_id:
            autor = User.objects.get(id=autor_id)
            Post.objects.create(titulo=titulo, corpo=corpo, autor=autor, publicado_em=publicado_em, pdf=pdf)
            messages.success(request, 'Post criado com sucesso.')
            return redirect('forum')  
        else:
            messages.error(request, 'Erro ao criar o post. Por favor, preencha todos os campos.')

    return render(request, 'app_cc/aluno/forum_novo.html')

@login_required
def apagar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.autor:
        post.delete()
        messages.success(request, 'Post apagado com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para apagar este post.')
    return redirect('forum')  

@login_required
def curtir_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.curtir(request.user):
        pass
    else:
        pass
    return redirect('forum')  

@has_role_or_redirect(Aluno)
def vocorrencias(request):
    user_reviews = Review.objects.filter(aluno__usuario=request.user)
    return render(request, 'app_cc/aluno/vocorrencias.html', {'user_reviews': user_reviews})
@has_role_or_redirect(Professor)
def ocorrenciasp(request):
    alunos = AlunoModel.objects.all()  # Recupera todos os alunos cadastrados
    print("nao entra no debug")
    if request.method == "POST":
        print("teste")
        title = request.POST.get('title')
        print(title)
        content = request.POST.get('content')
        print(content)
        aluno_id = request.POST.get('aluno')
        print(f"id do aluno: {aluno_id}")
        data_ocorrencia_str = request.POST.get('data_ocorrencia')  # Captura a data da ocorrência como string
        data_ocorrencia = parse_date(data_ocorrencia_str)  # Converte a string da data para um objeto date
        print(f"data da ocorrencia: {data_ocorrencia}")

        if title and content and aluno_id and data_ocorrencia:
            aluno = AlunoModel.objects.get(id=aluno_id)  # Obtém o objeto Aluno correspondente ao ID
            Review.objects.create(title=title, content=content, aluno=aluno, data_ocorrencia=data_ocorrencia)
            messages.success(request, 'Ocorrência enviada com sucesso.')
            return redirect('ocorrenciasp')  # Redireciona para a página desejada
    alunos = AlunoModel.objects.all()
    return render(request, 'app_cc/professor/ocorrenciasp.html', {'alunos': alunos})

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@login_required
def forum_view(request):
    posts = Post.objects.all()
    return render(request, 'app_cc/aluno/forum.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        corpo = request.POST.get('corpo')
        autor_id = request.user.id  # Assume que o usuário está autenticado
        publicado_em = timezone.now()
        pdf = request.FILES.get('pdf')  # Assume que o formulário tem um campo de upload de arquivo para o pdf

        if titulo and corpo and autor_id:
            autor = User.objects.get(id=autor_id)
            Post.objects.create(titulo=titulo, corpo=corpo, autor=autor, publicado_em=publicado_em, pdf=pdf)
            messages.success(request, 'Post criado com sucesso.')
            return redirect('forum')  
        else:
            messages.error(request, 'Erro ao criar o post. Por favor, preencha todos os campos.')

    return render(request, 'app_cc/aluno/forum_novo.html')

@login_required
def apagar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.autor:
        post.delete()
        messages.success(request, 'Post apagado com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para apagar este post.')
    return redirect('forum')  

@login_required
def curtir_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.curtir(request.user):
        pass
    else:
        pass
    return redirect('forum')  


def aluno_atividades(request):
    aluno = None
    atividades = None
    turma = None

    if AlunoModel.objects.filter(usuario=request.user).exists(): # sempre vai passar
        aluno = AlunoModel.objects.get(usuario=request.user)
        if aluno.turma:
            turma = aluno.turma
        atividades = Atividade.objects.filter(turma=aluno.turma)
        
        conclusao_atividade = []
        for atividade in atividades:
            if AtividadeFeita.objects.filter(atividade=atividade, conclusao=True, aluno = aluno):
                conclusao_atividade.append(True)
            else:
                conclusao_atividade.append(False)

        _atividades = zip(atividades, conclusao_atividade)

        if request.method != 'POST':
            return render(request, 'app_cc/aluno/atividades.html', {
                'zip': _atividades,
                'aluno': aluno,
                'turma': turma,
            })
        else:
            filtro = request.POST.get('filtrar')
            novas_atividades = []
            conclusao_atividade2 = []

            if filtro == 'T':
                return redirect('aluno_atividades')

            for atividade in atividades:
                if filtro == 'S':
                    if AtividadeFeita.objects.filter(atividade=atividade, conclusao=True):
                        novas_atividades.append(atividade)
                        conclusao_atividade2.append(True)
                else:
                    if AtividadeFeita.objects.filter(atividade=atividade, conclusao=False) or not AtividadeFeita.objects.filter(atividade=atividade).exists():
                        novas_atividades.append(atividade)
                        conclusao_atividade2.append(False)

            atividades_filtradas = list(zip(novas_atividades, conclusao_atividade2))
            return render(request, 'app_cc/aluno/atividades.html', {
                'zip': atividades_filtradas,
                'aluno': aluno,
                'turma': turma,
            })
    else:
        raise Http404()
        
@login_required
def aluno_atividade(request, id):
    if Atividade.objects.filter(id=id) and AlunoModel.objects.filter(usuario=request.user).exists():
        atividade = Atividade.objects.get(id=id)
        aluno = AlunoModel.objects.get(usuario=request.user)

        atividadeFeita = False
        if AtividadeFeita.objects.filter(atividade=atividade, conclusao=True, aluno=aluno):
            atividadeFeita = True

        if request.method != 'POST':
            return render(request, 'app_cc/aluno/atividade.html', {
                'atividade': atividade,
                'aluno': aluno,
                'atividadeFeita': atividadeFeita,
            })
        
        arquivo = request.FILES.get('arquivo')
        if not atividadeFeita:
            if arquivo:
                obj = AtividadeFeita.objects.create(atividade=atividade, conclusao=True, arquivo=arquivo, aluno=aluno)
                obj.save()
            else:
                messages.error(request, 'Envie o seu arquivo de resposta da atividade. É obrigatório.')
                return render(request, 'app_cc/aluno/atividade.html', {
                    'atividade': atividade,
                    'aluno': aluno,
                    'atividadeFeita': atividadeFeita,
                })
        
        atividadeFeita = True
        return render(request, 'app_cc/aluno/atividade.html', {
            'atividade': atividade,
            'aluno': aluno,
            'atividadeFeita': atividadeFeita,
        })

    else:
        raise Http404()


@has_role_or_redirect(Professor)
def atividades_professor(request):
    if ProfessorModel.objects.filter(usuario=request.user).exists():
        professor = ProfessorModel.objects.get(usuario=request.user)
        atividades = Atividade.objects.filter(professor=professor)

        _atividade = []
        realizacao_atividades = []
        print(atividades)
        for atividade in atividades:
            _atividade.append(atividade)
            print(atividades)
            x = list(AtividadeFeita.objects.filter(atividade=atividade))
            if not x:
                realizacao_atividades.append(False)
            else:
                realizacao_atividades.append(x)

        _zip = list(zip(_atividade, realizacao_atividades))

        return render(request, 'app_cc/professor/atividades_professor.html', {
            'zip': _zip,
            'professor': professor,
        })
    else:
        raise Http404()

@has_role_or_redirect(Professor)
def cadastrar_atividades_professor(request):
    if ProfessorModel.objects.filter(usuario=request.user).exists():
        professor = ProfessorModel.objects.get(usuario=request.user)
        turmas = Turma.objects.all()
        disciplinas = Disciplina.objects.all()

        if request.method != 'POST':
            return render(request, 'app_cc/professor/cadastrar_atividade.html', {
                'turmas': turmas,
                'disciplinas': disciplinas,
            })
    
        arquivo = request.FILES.get('arquivo', None)
        turma = request.POST.get('turma')
        disciplina = request.POST.get('disciplina')
        titulo = request.POST.get('titulo')
        texto = request.POST.get('texto')

        if not Turma.objects.filter(nome=turma).exists():
            messages.error(request, 'Essa turma não existe')
            if request.method != 'POST':
                return render(request, 'app_cc/professor/cadastrar_atividade.html', {
                    'turmas': turmas,
                    'disciplinas': disciplinas,
                })
            
        turma = Turma.objects.get(nome=turma)

        if not Disciplina.objects.filter(nome=disciplina).exists():
            messages.error(request, 'Essa disciplina não existe')
            if request.method != 'POST':
                return render(request, 'app_cc/professor/cadastrar_atividade.html', {
                    'turmas': turmas,
                    'disciplinas': disciplinas,
                })
            
        disciplina = Disciplina.objects.get(nome=disciplina)

        atividade = Atividade.objects.create(turma=turma, 
                                             disciplina=disciplina,
                                             arquivo=arquivo, 
                                             titulo=titulo, 
                                             texto=texto,
                                             professor=professor,
                                            )
        atividade.save()

        messages.success(request, 'Atividade cadastrada com sucesso!')
        return redirect('atividades_professor')

    else:
        raise Http404()
