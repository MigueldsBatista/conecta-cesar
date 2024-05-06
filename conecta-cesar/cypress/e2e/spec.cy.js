/* 
Pra iniciar 
npm init
npm install cypress --save -include=dev 
npx cypress open
 */
// Testes para usuários do tipo Professor

//Foi criado o comando "py ./manage.py tests" para criar os perfis de aluno e professor, esse comando sera executado no workflows da azure para garantir que os testes sejam realizados com sucesso o comando esta em app_cc/management/commands/tests.py
// Testes para usuários do tipo Professor
describe('Test Suite for Professors', () => {
  // Loga no início de cada teste como "professor1"
  beforeEach(() => {
    cy.visit('/auth/login/');
    cy.get('[type="text"]').type('professor1'); // Nome de usuário
    cy.get(':nth-child(3) > .form-control').type('123'); // Senha
    cy.get('.btn').click(); // Loga no sistema
  });

  it('Página Inicial', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('.navbar-nav > :nth-child(1) > .nav-link').click(); // Clica em Home
  });

  it('Disciplina', () => {
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

  it('Frequência', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('.dropdown > .nav-link').click(); 
    cy.get(':nth-child(2) > .dropdown-item').click(); // Frequência
    cy.get('div > input').click()
    cy.get('.btn').click()

    
  });

  it('Perfil', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(4) > .nav-link').click(); // Perfil
    
    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get(':nth-child(2) > .form-control').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });

    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get('.form-control').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia o arquivo funcional
        mimeType: 'image/png',
      });
    });

    cy.get('.btn').click();
    //cy.get('img').should('be visible'); // Verifica se a imagem do perfil é visível
  });

  it('Diário', () => {
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

  it('Página Principal', () => {
    cy.get('.navbar-toggler-icon').click(); 
    cy.get(':nth-child(1) > .nav-link').click(); // Página principal
  });

  it('Calendário', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(2) > .nav-link').click(); 
    cy.get('.fa-angle-right').click(); // Próximo mês
    cy.get('.fa-angle-left').click(); // Mês anterior
  });

  it('Boletim', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get('.dropdown > .nav-link').click(); 
    cy.get(':nth-child(1) > .dropdown-item').click()
    cy.get('#link_boletim').click()
    cy.get('.bar-container')//Vai pegar a barra do container

  });
  it('Perfil', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(4) > .nav-link').click(); // Acessa o perfil
    
    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get(':nth-child(2) > .form-control').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });

    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get('.form-control').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia a Foto de perfil funcional
        mimeType: 'image/png',
      });
    });

    //cy.get('.btn').click();
    //cy.get('img').should('be visible'); // Verifica se a imagem do perfil é visível
  });

  it('Hora extra', () => {
    cy.get('.navbar-toggler').click(); 
    cy.get(':nth-child(5) > .nav-link').click(); // Acessa Horas extras
    
    cy.fixture('pdfTeste.pdf').then((fileContent) => {
      cy.get(':nth-child(2) > .form-control').attachFile({
        fileContent,
        fileName: 'pdfTeste.pdf', //Envia um arquivo não funcional esperando que o sistema não aceite 
        mimeType: 'application/pdf', 
      });
    });


    cy.fixture('fotoTeste.png').then((fileContent) => {
      cy.get(':nth-child(2) > .form-control').attachFile({
        fileContent,
        fileName: 'fotoTeste.png',//Envia um arquivo funcional
        mimeType: 'image/png',
      });
      cy.get(':nth-child(3) > .form-control').type('15')
      cy.get('.mb-4 > .btn').click()//Enviar

      cy.get(':nth-child(1) > .text-center > :nth-child(1) > .form-control').type('10')
      cy.get(':nth-child(1) > .text-center > :nth-child(1) > .btn').click()//atualizar
     

      cy.get(':nth-child(1) > .text-center > :nth-child(2) > .btn').click()//Excluir

    });
    it('Diario', () => {
      cy.get('.navbar-toggler').click(); 
      cy.get(':nth-child(6) > .nav-link').click(); 
      cy.get('.list-group > :nth-child(1)')
    });  
    
  });
});
