/* 
deletar o diretorio nodule modules

deletar os packages .json


Pra iniciar 
npm init
npm install cypress --save -include=dev 
npm install --save-dev cypress-file-upload
npx cypress open
 */
// Testes para usuários do tipo Professor

//Foi criado o comando "py ./manage.py tests" para criar os perfis de aluno e professor, esse comando sera executado no workflows da azure para garantir que os testes sejam realizados com sucesso o comando esta em app_cc/management/commands/tests.py
// Testes para usuários do tipo Professor
describe('Test Suite - Setup and Tests', () => {
  before(() => {
    // Renomeia o banco de dados existente, se houver
    cy.exec('if [ -f db.sqlite3 ]; then mv db.sqlite3 db_backup.sqlite3; fi', { failOnNonZeroExit: false });
    
    cy.exec("cd ..", { failOnNonZeroExit: false }); // Sobe um diretório
    cy.exec("cd ..", { failOnNonZeroExit: false }); // Sobe um diretório
    cy.exec("rm db.sqlite3", { failOnNonZeroExit: false }); // Remove banco de dados existente
    cy.exec("python3 manage.py makemigrations", { failOnNonZeroExit: false }); // Executa migração do banco de dados
    cy.exec("python3 manage.py migrate", { failOnNonZeroExit: false }); // Executa migração do banco de dados
    cy.exec("python3 manage.py tests", { failOnNonZeroExit: false });
  });


  it('Caso de teste para verificar se o banco de dados foi recriado e migrações foram aplicadas', () => {
    // Comando para listar arquivos no diretório atual para confirmar que o banco de dados foi recriado
    cy.exec("ls").then((result) => {
      const files = result.stdout.split('\n'); // Divide a saída para obter uma lista de arquivos
      expect(files).to.include('db.sqlite3'); // Verifica se o banco de dados está presente
    });
  });

  it('Caso de teste para executar um teste simples para garantir que o ambiente está configurado corretamente', () => {
    // Verifica se o comando anterior foi bem-sucedido e se o teste pode ser executado
    expect(true).to.be.true; // Exemplo simples para garantir que o teste funciona
  });
});
describe('Test Suite for Professors', () => {
  // Loga no início de cada teste como "professor1"
  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000/pt/auth/login/');
    cy.get('#login-input').type('professor1'); // Nome de usuário
    cy.get(':nth-child(3) > .form-text-input > #password-input').type('123'); // Senha
    cy.get('.btn').click(); // Loga no sistema
    cy.visit('http://127.0.0.1:8000/pt/app/professor/avisosp/');

    
  });

  it('Caso de teste Página Inicial do Professor', () => {

      cy.get('.news-item').within(() => {
        cy.contains('E2E aviso').should('be.visible');//corresponde se o titulo corresponde ao mesmo que criamos no comando tests
      }); 
      
      cy.get('.news-item > .orange-text').click()
  
      cy.get('.container > :nth-child(2)').within(() => {
        cy.contains('testes automatizados').should('be.visible');//testa se a descrição do nosso aviso criado no comando tests corresponde com a descrição do aviso da página
      }); 

      //Faltando
  });

  it('Caso de teste Disciplinas do Professor', () => {
    cy.get('#navbar-link').click(); 
    cy.get('#turmas-dropdown > .nav-link').click(); 
    cy.get('#turmas-dropdown > .dropdown-menu > :nth-child(1) > .dropdown-item').click(); // Acessa disciplinas

    cy.get(':nth-child(3) > .table-container > tbody > :nth-child(2) > :nth-child(3) > .form-text-input > input').clear().type('-1')//digite -1 e deve falhar
    cy.get('.send').click();

    cy.get(':nth-child(3) > .table-container > tbody > :nth-child(2) > :nth-child(3) > .form-text-input > input').clear().type('11')//digite 11 e nao deve funcionar
    cy.get('.send').click();

    cy.get(':nth-child(3) > .table-container > tbody > :nth-child(2) > :nth-child(3) > .form-text-input > input').clear().type('6')//agora deve funcionar
    cy.get('.send').click();
  });

  it('Caso de teste Área Desempenho do Professor', () => {
    cy.get('#navbar-link').click(); 
    cy.get('#turmas-dropdown > .nav-link').click(); 
    cy.get('#turmas-dropdown > .dropdown-menu > :nth-child(3) > .dropdown-item').click(); // Acessa "Desempenho"

    cy.get("#nota-valor").invoke('text').then((nota) => {
      // Remove a vírgula e converte para float
      const notaNumerica = parseFloat(nota.replace(',', '.')); 
      expect(notaNumerica).to.be.lessThan(7);
  });
  cy.get("#falta-valor").invoke('text').then((falta) => {
    // Remove a vírgula e converte para float
    const faltaNumerica = parseFloat(falta.replace(',', '.')); 
    expect(faltaNumerica).to.be.greaterThan(8);
});
  });

  it('Caso de teste Frequência do Professor', () => {
    cy.get('#navbar-link').click(); 
    cy.get('#turmas-dropdown > .nav-link').click(); 
    cy.get('#turmas-dropdown > .dropdown-menu > :nth-child(2) > .dropdown-item').click(); // Frequência
    
    cy.get(':nth-child(3) > :nth-child(1) > ul > li > div > input').click();
    cy.get('.send').click();


    cy.get(':nth-child(3) > :nth-child(1) > ul > li > span').invoke('text').then((badgeValue) => {
      cy.wrap(badgeValue).as('badgeValue'); // Salva a quantidade de faltas
    });
    cy.get('.send').click(); //Tenta clicar novamente em registrar uma falta
    cy.get('@badgeValue').then((badgeValue) => {
      cy.get(':nth-child(3) > :nth-child(1) > ul > li > span').invoke('text').should('equal', badgeValue); //Verifica a quantidade de faltas não mudou
    });

  });

  it('Caso de teste Área do Professor', () => {

    cy.get('#navbar-link').click(); 
    cy.get('#turmas-dropdown > .nav-link').click(); 
    cy.get('#sala-link').click(); // Acessa disciplinas
    cy.get("#file-input").attachFile("fotoTeste.png");//Envia uma foto png e deve funcionar
    cy.get('#slide_titulo_input').type("titulo")
    cy.get('#slide_descricao_input').type("descricao")
    cy.get('#disciplina-input').select("Disciplina 1")
    cy.get(".send").click();
    cy.get('.alert').should('be.visible')

    cy.get("#file-input").attachFile("fotoTeste.png");//Envia um pdf e deve funcionar
    cy.get('#slide_titulo_input').type("titulo")
    cy.get('#slide_descricao_input').type("descricao")
    cy.get('#disciplina-input').select("Disciplina 1")
    cy.get(".send").click();
    cy.get('.alert').should('be.visible')


    //envia sem um arquivo e deve funcionar
    cy.get('#slide_titulo_input').type("titulo")
    cy.get('#slide_descricao_input').type("descricao")
    cy.get('#disciplina-input').select("Disciplina 1")
    cy.get(".send").click();
    cy.get('.alert').should('be.visible')




  });

  it('Caso de teste Calendário do Professor', () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const day = String(today.getDate()).padStart(2, '0');
    const currentDate = `${year}-${month}-${day}`; // Formato YYYY-MM-DD

    cy.get('#navbar-link').click(); 
    cy.get('#calendario-link').click(); 
    cy.get('.today').click();//O dia atual deve estar em destaque
    


    cy.get("#titulo").type("titulo")
    cy.get("#descricao").type("descricao")
    cy.get("#data").type(currentDate)
    cy.get("#horario").type("12:30")

    cy.get("#disciplina").select("Disciplina 1")
    cy.get('.send').click()

    cy.get(".event-day").should("exist")


  });

  it('Caso de teste Diário do Professor', () => {
    cy.get('#navbar-link').click(); 
    cy.get(':nth-child(4) > .nav-link').click(); // Acessa o diário
    cy.get('#disciplina-select').select('Disciplina 1');
    cy.get('#titulo-input').type('titulo')
    cy.get('#descricao-input').type('conteudo')
    cy.get('.send').click()
    });

  it('Caso de teste Perfil do Professor', () => {
    cy.get('#navbar-link').click(); 
    cy.get(':nth-child(5) > .nav-link').click(); // Perfil
    
    cy.get('.send').click();//Tenta clicar no botão de enviar arquivo sem nenhum arquivo
    cy.get('.alert').within(() => {
      // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
      cy.contains('Por favor, envie uma nova foto de perfil.').should('be.visible');
    }); // O alerta não deve estar presente


    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get('#foto_perfil').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });
    cy.get('.send').click()
    cy.get('.alert').within(() => {
      // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
      cy.contains('Somente arquivos JPG ou PNG são permitidos.').should('be.visible');
    });

    
    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get('#foto_perfil').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia o arquivo funcional
        mimeType: 'image/png',
      });
    });

    cy.get('.send').click();
    cy.get('.alert').within(() => {
    cy.contains('Foto de perfil atualizada com sucesso!').should('be.visible');//Mensagem de sucesso
    });
  });
});

// Testes para usuários do tipo Aluno
describe('Test Suite for Students', () => {
  // Loga o aluno antes de cada teste como "aluno1"
  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000/pt/auth/login/');
    cy.get('#login-input').type('aluno1'); // Nome de usuário
    cy.get(':nth-child(3) > .form-text-input > #password-input').type('123'); // Senha
    cy.get('.btn').click(); // Loga no sistema
    cy.visit('http://127.0.0.1:8000/pt/app/aluno/avisos/');
  });

  it('Caso de teste Página Principal do Aluno', () => {


      cy.get('.news-item').within(() => {
      cy.contains('E2E aviso').should('be.visible');//corresponde se o titulo corresponde ao mesmo que criamos no comando tests
    }); 
    
    cy.get('.news-item > .orange-text').click()
    cy.get('.container > :nth-child(2)').within(() => {
      cy.contains('testes automatizados').should('be.visible');//testa se a descrição do nosso aviso criado no comando tests corresponde com a descrição do aviso da página
    }); 
  });

  it('Caso de teste Calendário do Aluno', () => {
    cy.visit('http://127.0.0.1:8000/pt/app/aluno/calendario/');
    cy.get(".today").click();

    cy.get('.custom-event-details > :nth-child(1)').within(() => {
      cy.contains('Disciplina 1').should('be.visible');//o evento deve estar associado a disciplina criada no evento
      cy.contains('evento e2e').should('be.visible');
    })

  });

  it('Caso de teste Boletim do Aluno', () => {

    cy.get('#navbar-link').click(); 
    cy.get('#avaliacao-link').click(); 
    cy.get('#boletim-link').click();
    cy.get('.grade-container > :nth-child(1)').within(() => {
      cy.contains('Disciplina 1').should('be.visible');//A disciplina aqui deve ser a criada e associada ao aluno no comando tests
    });

    cy.get('#link_boletim').click();

    

    cy.get('#notasChart');//Vai pegar a barra do container do gráfico da nota que deve aparecer

  });

  it('Caso de teste Frequência do Aluno', () => {

    cy.get('#navbar-link').click();
    cy.get('#avaliacao-link').click(); 
    cy.get('#frequencia-link').click();

  });

  it('Caso de teste Perfil do Aluno', () => {
    cy.get('#navbar-link').click(); 
    cy.get(':nth-child(4) > .nav-link').click(); // Acessa o perfil
    
    cy.get('.send').click();//Tenta clicar no botão de enviar arquivo sem nenhum arquivo
    cy.get('.alert').within(() => {
      // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
      cy.contains('Por favor, envie uma nova foto de perfil.').should('be.visible');
    });
 // O alerta não deve estar presente

    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get('#foto_perfil').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });
    cy.get('.send').click()
    cy.get('.alert').within(() => {
      // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
      cy.contains('Somente arquivos JPG ou PNG são permitidos.').should('be.visible');
    });



    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get('#foto_perfil').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia a Foto de perfil funcional
        mimeType: 'image/png',
      });
    });
    cy.get('.send').click();
    cy.get('.alert').within(() => {
      
      cy.contains('Foto de perfil atualizada com sucesso!').should('be.visible');//Mensagem de sucesso
    });
  });

  it('Caso de teste Horas extras do Aluno', () => {
    cy.get('#navbar-link').click(); 
    cy.get(':nth-child(5) > .nav-link').click(); // Acessa Horas extras

    cy.get('.send').click()//Enviar
    cy.get('.alert').should('not.exist')
    
    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get('#file-input').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });
    cy.get(':nth-child(2) > .form-text-input > .form-control').type('15')
    cy.get('.send').click()//Enviar 
    cy.get('.alert').within(() => {
      // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
      cy.contains('Somente arquivos JPG ou PNG são permitidos.').should('be.visible');
    });
    

    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get('#file-input').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia um arquivo funcional
        mimeType: 'image/png',
      });
      cy.get(':nth-child(2) > .form-text-input > .form-control').clear().type('15')
      cy.get('.send').click()//Enviar

      cy.get(':nth-child(1) > .d-flex > #myForm > .form-text-input > .form-control').type('10')
      cy.get(':nth-child(1) > .d-flex > #myForm > .update-button').click()//atualizar
     

      cy.get(':nth-child(1) > .d-flex > :nth-child(2) > .delete-button').click()//Excluir
      cy.get('.alert').within(() => {
        // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
        cy.contains('Arquivo excluído com sucesso.').should('be.visible');
      }); 
      

    });    
  });
  it('Diario do Aluno', () => {
    cy.get('#navbar-link').click(); 
    cy.get(':nth-child(6) > .nav-link').click(); 
    cy.get('.list-group > :nth-child(1)')
  });  
});

after(() => {
  // Remove o banco de dados de testes
  cy.exec("rm db.sqlite3", { failOnNonZeroExit: false });
  // Restaura o banco de dados original, se houver
  cy.exec('if [ -f db_backup.sqlite3 ]; then mv db_backup.sqlite3 db.sqlite3; fi', { failOnNonZeroExit: false });
});
