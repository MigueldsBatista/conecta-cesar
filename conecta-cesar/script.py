import os
import subprocess
import shutil
import time
import webbrowser
import urllib.request  # Adicionando o módulo para baixar o get-pip.py

def deletar_venv():
    # Verificar se o diretório venv existe e deletá-lo se existir
    if os.path.exists('venv'):
        try:
            shutil.rmtree('venv')
        except Exception as e:
            print("Erro ao deletar o diretório venv:", e)

def criar_env():
    with open('.env', 'w') as arquivo_env:
        arquivo_env.write('TARGET_ENV=Dev\n')

def criar_venv():
    # Criar um novo ambiente virtual
    subprocess.Popen(['py', '-m', 'venv', 'venv'])

def instalar_pip():
    # Tentar instalar o pip usando 'py'
    try:
        subprocess.Popen(['py', 'get-pip.py'])
    # Se não for possível instalar o pip com 'py', tentar com 'python'
    except FileNotFoundError:
        try:
            subprocess.Popen(['python', 'get-pip.py'])
        # Se 'python' também não estiver disponível, exibir uma mensagem de erro
        except FileNotFoundError:
            print("Erro: Não foi possível instalar o pip.")
            return


def iniciar_servidor():
    # Deletar o ambiente virtual existente
    deletar_venv()
    
    # Criar um novo ambiente virtual
    criar_venv()

    criar_env()

    # Tenta ativar o ambiente virtual usando o comando 'py'
    try:
        subprocess.Popen([r'venv\Scripts\activate'], shell=True)
    # Se não for possível ativar o ambiente virtual com 'py', tenta com 'python'
    except FileNotFoundError:
        try:
            subprocess.Popen(['python', '-m', 'venv', 'venv'])
            subprocess.Popen([r'venv\Scripts\activate'], shell=True)
        # Se 'python' também não estiver disponível, exibe uma mensagem de erro
        except FileNotFoundError:
            print("Erro: Não foi possível criar ou ativar o ambiente virtual.")
            return
    
    time.sleep(1)  # Esperar um pouco para que o ambiente virtual seja ativado
    instalar_pip()
    # Tentar instalar os pacotes usando 'pip'
    try:
        subprocess.Popen(['pip', 'install', '-r', 'requirements.txt'])
    # Se 'pip' não for encontrado, tentar usar 'python -m pip'
    except FileNotFoundError:
        try:
            subprocess.Popen(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])
        # Se 'python -m pip' também não for encontrado, exibir uma mensagem de erro
        except FileNotFoundError:
            print("Erro: Não foi possível instalar os requisitos.")
            return

    subprocess.Popen(['py', './manage.py', 'runserver'])

def abrir_link_no_navegador(url):
    # Tenta abrir o link no navegador padrão do sistema
    try:
        webbrowser.open(url)
    except Exception as e:
        print("Erro ao abrir o navegador:", e)

if __name__ == "__main__":
    # Iniciar o servidor Django e aguardar alguns segundos
    iniciar_servidor()
    
    # Aguardar um pouco para o servidor iniciar
    time.sleep(2)  

    # Abrir o navegador no endereço do servidor
    abrir_link_no_navegador('http://127.0.0.1:8000')
