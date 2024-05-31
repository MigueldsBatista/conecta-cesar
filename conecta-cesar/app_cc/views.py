from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Disciplina, Nota, Diario, Professor as ProfessorModel, Aluno as AlunoModel, Falta, File, Evento, Aviso, Relatorio, ProfessorFile 
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
    aluno = request.user.aluno  # Obtém o aluno logado
    disciplinas = aluno.turma.disciplinas.all()
    print(disciplinas)
    eventos = Evento.objects.filter(disciplina__in=disciplinas)  # Filtra os eventos pelas disciplinas do aluno
    print(eventos)
    eventos_list = list(eventos.values('titulo', 'descricao', 'data', 'horario', 'disciplina__nome'))
    eventos_json = json.dumps(eventos_list, default=str)  # Serializa os eventos para JSON

    context = {
        'eventos_json': eventos_json
    }
    return render(request, 'app_cc/aluno/calendario.html', context)

#----------------------------------------------------------------------------------------------------------------    
#----------------------------------------PROFESSOR VIEWS---------------------------------------------------------  
#---------------------------------------------------------------------------------------------------------------- 

@has_role_or_redirect(Professor)
def slidesp(request):
    # Obter o professor associado ao usuário autenticado
    professor = ProfessorModel.objects.get(usuario=request.user)

    disciplinas = Disciplina.objects.filter(professor=professor)


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


        # Verificar se o tipo do arquivo é aceitável
        if file:
            ext_permitidas = ('.jpg', '.jpeg', '.png', '.pdf', '.pptx', '.docx')
            if not file.name.lower().endswith(ext_permitidas):
                messages.error(request, _("Tipo de arquivo não permitido (Tipos aceitos: '.jpg', '.jpeg', '.png', '.pdf', '.pptx', '.docx')."))
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
            archive.save()
        else:
            archive = ProfessorFile(
                titulo=titulo,
                descricao=descricao,
                professor=professor,
            )
            archive.save()

        messages.success(request, _("Documento salvo com sucesso."))
        return redirect("slidesp")
    
    # Após lidar com POST, renderizar com 'ext' no contexto
    arquivos = ProfessorFile.objects.filter(professor=professor)
    return render(
        request,
        "app_cc/professor/slidesp.html",
        {"arquivos": arquivos},
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
            'eventos_json': eventos_json  # Passando os eventos serializados
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


#----------------------------------------------------------------------------------------------------------------    
@has_role_or_redirect(Professor)
def boletimp(request):
    professor = ProfessorModel.objects.get(usuario=request.user)
    disciplinas = Disciplina.objects.filter(professor=professor)
        # Manter um único relatório, se múltiplos existem


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
                                messages.error(request, _("A nota deve estar entre 0 e 10."))
                                return redirect("boletimp")

                            nota, created = Nota.objects.get_or_create(
                                disciplina=disciplina,
                                aluno=aluno
                            )
                            nota.valor = nota_float
                            nota.save()
                            gerar_relatorio(disciplinas, professor)




                        except ValueError:
                            messages.error(request, _("Valor inválido para nota."))
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
                    'nota': nota_valor,
                    
                })

        disciplinas_com_turmas_e_alunos.append(disciplina_info)

    return render(
        request,
        'app_cc/professor/boletimp.html',
        {'disciplinas_com_turmas_e_alunos': disciplinas_com_turmas_e_alunos}
    )