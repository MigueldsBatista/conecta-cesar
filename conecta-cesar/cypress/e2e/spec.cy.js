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
  // Executa comandos antes de todos os testes no arquivo
  before(() => {
    cy.exec("cd ..", { failOnNonZeroExit: false }); // Sobe um diretório
    cy.exec("cd ..", { failOnNonZeroExit: false }); // Sobe um diretório
    cy.exec("rm db.sqlite3", { failOnNonZeroExit: false }); // Remove banco de dados
    cy.exec("python3 manage.py makemigrations", { failOnNonZeroExit: false }); // Executa migração do banco de dados
    cy.exec("python3 manage.py migrate", { failOnNonZeroExit: false }); // Executa migração do banco de dados
    cy.exec("python3 manage.py tests", { failOnNonZeroExit: false });
    cy.exec("python3 manage.py runserver", { failOnNonZeroExit: false });

     // Executa testes Django
  });

  it('Test Case Verifica se o banco de dados foi recriado e migrações foram aplicadas', () => {
    // Comando para listar arquivos no diretório atual para confirmar que o banco de dados foi recriado
    cy.exec("ls").then((result) => {
      const files = result.stdout.split('\n'); // Divide a saída para obter uma lista de arquivos
      expect(files).to.include('db.sqlite3'); // Verifica se o banco de dados está presente
    });
  });

  it('Test Case Executa um teste simples para garantir que o ambiente está configurado corretamente', () => {
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

  it('Test Case Página Inicial do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('.navbar-nav > :nth-child(1) > .nav-link').click(); // Clica em Home
  });

  it('Test Case Disciplinas do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('.dropdown > .nav-link').click(); 
    cy.get(':nth-child(1) > .dropdown-item').click(); // Acessa disciplinas

    cy.get(':nth-child(3) > input').type('-1')//digitar a nota -1
    cy.get('.btn').click();

    cy.get(':nth-child(3) > input').clear().type('11')//tenta digitar a nota 11
    cy.get('.btn').click();

    cy.get(':nth-child(3) > input').clear().type('10')//digita nota 10
    cy.get('.btn').click();
  });

  it('Test Case Frequência do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('.dropdown > .nav-link').click(); 
    cy.get(':nth-child(2) > .dropdown-item').click(); // Frequência
    cy.get('div > input').click()
    cy.get('.btn').click()//Registra a falta


    cy.get('.badge').invoke('text').then((badgeValue) => {
      cy.wrap(badgeValue).as('badgeValue'); // Salva a quantidade de faltas
    });
    cy.get('.btn').click(); //Tenta clicar novamente em registrar uma falta
    cy.get('@badgeValue').then((badgeValue) => {
    cy.get('.badge').invoke('text').should('equal', badgeValue); //Verifica a quantidade de faltas não mudou
    });

  });

  it('Test Case Perfil do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(4) > .nav-link').click(); // Perfil
    
    cy.get('.btn').click();//Tenta clicar no botão de enviar arquivo sem nenhum arquivo
     cy.get('.alert').should('not.exist'); // O alerta não deve estar presente


    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get(':nth-child(2) > .form-control').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });
    cy.get('.btn').click()
    cy.get('.alert').within(() => {
      // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
      cy.contains('Somente arquivos JPG ou PNG são permitidos.').should('be.visible');
    });

    
    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get('.form-control').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia o arquivo funcional
        mimeType: 'image/png',
      });
    });

    cy.get('.btn').click();
    cy.get('.alert').within(() => {
    cy.contains('Foto de perfil atualizada com sucesso!').should('be.visible');//Mensagem de sucesso
    });
  });

  it('Test Case Diário do Professor', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(5) > .nav-link').click(); // Acessa o diário
    cy.get('#tituloDiario').type('diario')
    cy.get('#textoDiario').type('conteudo')
    cy.get('.btn').click()
    });
});

// Testes para usuários do tipo Aluno
describe('Test Suite for Students', () => {
  // Loga o aluno antes de cada teste como "aluno1"
  beforeEach(() => {
    cy.visit('/auth/login/');
    cy.get('[type="text"]').type('aluno1'); // Nome de usuário
    cy.get(':nth-child(3) > .form-control').type('123'); // Senha
    cy.get('.btn').click(); // Loga no sistema
  });

  it('Test Case Página Principal do Aluno', () => {
    cy.get('.navbar-toggler-icon').click(); 
    cy.get(':nth-child(1) > .nav-link').click(); // Página principal
  });

  it('Test Case Calendário do Aluno', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(2) > .nav-link').click(); 
    cy.get('.fa-angle-right').click(); // Próximo mês
    cy.get('.fa-angle-left').click(); // Mês anterior
  });

  it('Test Case Boletim do Aluno', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('.dropdown > .nav-link').click(); 
    cy.get(':nth-child(1) > .dropdown-item').click()
    cy.get('#link_boletim').click()
    cy.get('#notasChart')//Vai pegar a barra do container do gráfico da nota que deve aparecer

  });
  it('Test Case Perfil do Aluno', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(4) > .nav-link').click(); // Acessa o perfil
    
    cy.get('.btn').click();//Tenta clicar no botão de enviar arquivo sem nenhum arquivo
     cy.get('.alert').should('not.exist'); // O alerta não deve estar presente

    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get(':nth-child(2) > .form-control').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });
    cy.get('.btn').click()
    cy.get('.alert').within(() => {
      // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
      cy.contains('Somente arquivos JPG ou PNG são permitidos.').should('be.visible');
    });



    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get('.form-control').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia a Foto de perfil funcional
        mimeType: 'image/png',
      });
    });
    cy.get('.btn').click();
    cy.get('.alert').within(() => {
      
      cy.contains('Foto de perfil atualizada com sucesso!').should('be.visible');//Mensagem de sucesso
    });
  });

  it('Test Case Horas extras do Aluno', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(5) > .nav-link').click(); // Acessa Horas extras

    cy.get('.mb-4 > .btn').click()//Enviar
    cy.get('.alert').should('not.exist')
    
    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get(':nth-child(2) > .form-control').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });
    cy.get(':nth-child(3) > .form-control').type('15')
    cy.get('.mb-4 > .btn').click()//Enviar 
    cy.get('.alert').within(() => {
      // Verifica se o texto "Somente arquivos JPG ou PNG são permitidos" está presente no formulário
      cy.contains('Somente arquivos JPG ou PNG são permitidos.').should('be.visible');
    });
    

    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get(':nth-child(2) > .form-control').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia um arquivo funcional
        mimeType: 'image/png',
      });
      cy.get(':nth-child(3) > .form-control').clear().type('15')
      cy.get('.mb-4 > .btn').click()//Enviar

      cy.get(':nth-child(1) > .text-center > :nth-child(1) > .form-control').type('10')
      cy.get(':nth-child(1) > .text-center > :nth-child(1) > .btn').click()//atualizar
     

      cy.get(':nth-child(1) > .text-center > :nth-child(2) > .btn').click()//Excluir

    });
    it('Test Case Diario do Aluno', () => {
      cy.get('.navbar-toggler').click(); 
      cy.get(':nth-child(6) > .nav-link').click(); 
      cy.get('.list-group > :nth-child(1)')
    });  
    
  });
});
