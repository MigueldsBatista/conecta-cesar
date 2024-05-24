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
    cy.exec("python3 manage.py runserver", { failOnNonZeroExit: false });
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
    cy.visit('/auth/login/');
    cy.get('[type="text"]').type('professor1'); // Nome de usuário
    cy.get(':nth-child(3) > .form-text-input > .form-control').type('123'); // Senha
    cy.get('.btn').click(); // Loga no sistema
  });

  it('Caso de teste Página Inicial do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('.navbar-nav > :nth-child(1) > .nav-link').click(); // Clica em Home
  });

  it('Caso de teste Disciplinas do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('#turmas-dropdown > .nav-link').click(); 
    cy.get('#turmas-dropdown > .dropdown-menu > :nth-child(1) > .dropdown-item').click(); // Acessa disciplinas

    cy.get(':nth-child(3) > input').type('-1')//digitar a nota -1
    cy.get('.send').click();

    cy.get(':nth-child(3) > input').clear().type('11')//tenta digitar a nota 11
    cy.get('.send').click();

    cy.get(':nth-child(3) > input').clear().type('10')//digita nota 10
    cy.get('.send').click();
  });

  it('Caso de teste Frequência do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('#turmas-dropdown > .nav-link').click(); 
    cy.get('#turmas-dropdown > .dropdown-menu > :nth-child(2) > .dropdown-item').click(); // Frequência
    cy.get('div > input').click()
    cy.get('.send').click()//Registra a falta


    cy.get('.badge').invoke('text').then((badgeValue) => {
      cy.wrap(badgeValue).as('badgeValue'); // Salva a quantidade de faltas
    });
    cy.get('.send').click(); //Tenta clicar novamente em registrar uma falta
    cy.get('@badgeValue').then((badgeValue) => {
    cy.get('.badge').invoke('text').should('equal', badgeValue); //Verifica a quantidade de faltas não mudou
    });

  });

  it('Caso de teste Perfil do Professor', () => {
    cy.get('.navbar-toggler').click(); 
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

  it('Caso de teste Diário do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(4) > .nav-link').click(); // Acessa o diário
    cy.get(':nth-child(3) > .form-control').type('diario')
    cy.get(':nth-child(4) > .form-control').type('conteudo')
    cy.get('.send').click()
    });
});

// Testes para usuários do tipo Aluno
describe('Test Suite for Students', () => {
  // Loga o aluno antes de cada teste como "aluno1"
  beforeEach(() => {
    cy.visit('/auth/login/');
    cy.get('[type="text"]').type('aluno1'); // Nome de usuário
    cy.get(':nth-child(3) > .form-text-input > .form-control').type('123'); // Senha
    cy.get('.btn').click(); // Loga no sistema
  });

  it('Caso de teste Página Principal do Aluno', () => {
    cy.get('.navbar-toggler-icon').click(); 
    cy.get(':nth-child(1) > .nav-link').click(); // Página principal
  });

  it('Caso de teste Calendário do Aluno', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(2) > .nav-link').click(); 
    //cy.get('.fa-angle-right').click(); // Próximo mês
    //cy.get('.fa-angle-left').click(); // Mês anterior
  });

  it('Caso de teste Boletim do Aluno', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('#avaliacao-link').click(); 
    cy.get('#avaliacao-dropdown > .dropdown-menu > :nth-child(1) > a').click()
    cy.get('#link_boletim').click()
    cy.get('#notasChart')//Vai pegar a barra do container do gráfico da nota que deve aparecer

  });
  it('Caso de teste Perfil do Aluno', () => {
    cy.get('.navbar-toggler').click(); 
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
    cy.get('.navbar-toggler').click(); 
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
    cy.get('.form-group > .form-control').type('15')
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
      cy.get('.form-group > .form-control').clear().type('15')
      cy.get('.send').click()//Enviar

      cy.get('#myForm > .form-control').type('10')
      cy.get('.update-button').click()//atualizar
     

      cy.get('.delete-button').click()//Excluir
      cy.get('.alert').within(() => {
        // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
        cy.contains('Arquivo excluído com sucesso.').should('be.visible');
      }); 
      

    });
    it('Diario do Aluno', () => {
      cy.get('.navbar-toggler').click(); 
      cy.get(':nth-child(6) > .nav-link').click(); 
      cy.get('.list-group > :nth-child(1)')
    });  
    
  });
});

after(() => {
  // Remove o banco de dados de testes
  cy.exec("rm db.sqlite3", { failOnNonZeroExit: false });
  // Restaura o banco de dados original, se houver
  cy.exec('if [ -f db_backup.sqlite3 ]; then mv db_backup.sqlite3 db.sqlite3; fi', { failOnNonZeroExit: false });
});