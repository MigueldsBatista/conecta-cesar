Esse arquivo serve pra explicar como funciona herança no django

Observações: herança não funciona quando você usa o preview do vs code, é necessário iniciar o servidor django pra conseguir vizualizar efetivamente as mudanças em tempo real

*pra iniciar o servidor django é muito fácil, pras etapas funcionarem é necessário que o repositório local seja idêntico ao do git que é oq eu to usando, caso contrário é so mudar o nome dos caminhos

* Recomendo que baixem a extensão de django pra vizualizar melhor os blocks e os códigos em python

Name: Django
Id: batisteo.vscode-django
Description: Beautiful syntax and scoped snippets for perfectionists with deadlines
Version: 1.15.0
Publisher: Baptiste Darthenay
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django

1- dentro da pasta CONECTA-CESAR clique com o botão direito no explorador de arquivos e selecione abrir no terminal

2- cd conecta-cesar

3- . conecta-cesar/Scripts/activate

4- py ./manage.py runserver

5- abra o link do servidor no navegador 


HERANÇA

basicamente herança em django consiste em ter um arquivo pai que vai servir de base pra todos os arquivos filhos herdarem suas características, isso facilita muito na hora de criar os códigos e fazer manutenção. Pra ficar mais facil de entender, no nosso site todos os arquivos possuem a navbar e o fundo laranja, então eu criei um arquivo pai chamado "main.html"(que serve pra todos os arquivos de ALUNOS) e outro arquivo pai chamado "mainp.html"(que serve pros arquivos de PROFESSORES) a única diferença são os itens que aparecem na navbar, mas então como fazer os arquivos filhos herdarem essas características dos pais

NO ARQUIVO PAI

você colocar todo o conteúdo que vai ser herdado pelas outras pagínas, no caso do nosso site, o conteudo do arquivo vai desde a head, os links, body, html, até a nav bar e estilo de fundo laranja, pq tudo isso vai se repetir nas outras páginas. Onde o conteúdo da página for ser diferente, por exemplo a aba de avisos você vai abrir um block, indicando que aquele trecho vai ser preenchido pelo conteúdo da pagina do html filho mas o que é um block?

BLOCKS
quando estamos usando django escrever {% %} quer dizer que o que está entre as chaves e a porcentagem vai ser lido como um código python e a tag block indica que vai um conteúdo html ali dentro.

voltando...ainda no arquivo pai você abre um 

{% block content %}no arquivo pai aqui fica VAZIO, porém no arquivo filho é onde vai o conteudo html {% endblock content %} 

(lembrando que content é uma variável, então pode assumir qualquer valor).

NO ARQUIVO FILHO 

no topo da página você vai indicar de qual página o filho está herdando o html escrevendo
{% extends "app_cc/main.html"} --> no caso do nosso site esse é o endereço

aqui no arquivo FILHO é onde você coloca o conteúdo específico da página filha todo o resto vai ser herdado da página pai
{% block content }

<h1>Avisos<h1>
<form>Um formulario</forms>
<p>um texto</p>

 {% endblock content %}

Aqui no repositório tem vários exemplos, tentem dar uma olhada pra entenderem na prática 

