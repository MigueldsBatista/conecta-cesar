# Contribuindo para o Projeto Conecta Cesar 🤝

Bem-vindo ao projeto Conecta Cesar! Estamos empolgados em ter você contribuindo para o desenvolvimento desta plataforma incrível para o universo escolar. Antes de começar, por favor, leia este guia para entender como você pode contribuir de maneira eficaz.

# Contribuindo para o Projeto

Obrigado por considerar contribuir para o nosso projeto! Siga as instruções abaixo para configurar o ambiente de desenvolvimento.

## Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado na sua máquina:

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Passos para Configuração

### 1. Clone o Repositório

Abra seu terminal e navegue até o diretório onde deseja clonar o repositório. Em seguida, execute o comando abaixo:

git clone https://github.com/MigueldsBatista/conecta-cesar.git

### 2. Navegue até o Diretório do Projeto
Use o comando

cd conecta-cesar/conecta-cesar

### 3. Crie e Ative um Ambiente Virtual
Para criar um ambiente virtual, execute o seguinte comando:

python -m venv venv

Para ativar o ambiente virtual:

No Windows:

.\venv\Scripts\activate

No macOS/Linux:

source venv/bin/activate

### 4. Instale as Dependências
Com o ambiente virtual ativado dentro da mesma pasta, instale as dependências necessárias:

pip install -r requirements.txt

### 5. Execute o Servidor de Desenvolvimento
Finalmente, para iniciar o servidor de desenvolvimento, execute:

python manage.py runserver
Agora, você deve ser capaz de acessar o aplicativo em seu navegador, normalmente em http://127.0.0.1:8000/.

### 6. Contribuindo com Código

Recomendamos o uso do Visual Studio Code (VSCode) para desenvolver o projeto. Para abrir o projeto no VSCode, siga os passos abaixo:

Abra o VSCode.
Clique em File > Open Folder... e selecione o diretório do projeto conecta-cesar.
Certifique-se de que o ambiente virtual esteja ativado no terminal do VSCode.

Para editar o código usamos
crie um Fork do repositório.
Clone seu fork localmente.
Crie uma branch para sua modificação:

git checkout -b minha-nova-feature
Faça suas mudanças.
Commit suas mudanças:

git commit -m "Adicionar nova feature"
Push para a branch:

git push origin minha-nova-feature
Abra um Pull Request.

### Processo de Revisão
Nossa equipe irá analisar todos os pull requests. Apenas aqueles que forem coerentes e estiverem alinhados com os objetivos do projeto serão aprovados.

Dúvidas?
Se tiver qualquer dúvida, sinta-se à vontade para abrir uma issue.




## Diretrizes de Desenvolvimento 🤔

  - Para fazer uma boa contribuição siga as boas práticas de codificação em Python, HTML e CSS.
  - Formatação correta do código.
  - Ordem de imports correta no código.
  - Caso qualquer um desses itens não seja validado, o Push não vai ser aprovado, e o Call Center vai pedir pra você melhorar o Pull Request. :D



Obrigado por contribuir para o Conecta Cesar! Este guia cobre os passos básicos para configurar o ambiente de desenvolvimento e contribuir com código. Se tiver alguma dúvida, não hesite em entrar em contato com a equipe de desenvolvimento.
