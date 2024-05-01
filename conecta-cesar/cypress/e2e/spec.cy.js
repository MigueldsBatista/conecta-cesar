describe('Test Suite for Multiple User Types', () => {
  let randomEmail;
  let randomName;


  beforeEach(() => {
    // Gera um email e um nome aleatórios
    const randomString = Math.random().toString(36).substring(2, 11);
    const randomNumber = Math.floor(Math.random() * 1000) + 1;

    randomEmail = `user_${randomString}@test.com`;
    randomName = `Name_${randomString}`;
  });


  it('Register as Professor', () => {
    cy.visit('');
    cy.get('a').click();
    cy.get('[type="text"]').type(randomName); // Usa o nome gerado
    cy.get('[type="email"]').type(randomEmail); // Usa o email gerado
    cy.get(':nth-child(3) > .form-control').type('123');
    cy.get('#user-type').select('professor'); // Define o tipo como 'admin'
    cy.get('.btn').click();
    cy.get(':nth-child(2) > .form-control').type(randomName); // Reutiliza o mesmo nome
    cy.get(':nth-child(3) > .form-control').type('123');
    cy.get('.btn').click();
    cy.get('.navbar-toggler').click()//Clica na barra de navegação
    cy.get('.navbar-nav > :nth-child(1) > .nav-link').click()//Clica em Home
    cy.get('.navbar-toggler').click() //Clica na barra de navegação
    cy.get('.dropdown > .nav-link').click()//Clica em Turmas
    cy.get(':nth-child(1) > .dropdown-item').click() //Clica em disciplinas
    cy.get('.navbar-toggler').click() //Clica na barra de navegação
    cy.get('.dropdown > .nav-link').click()//Clica em Turmas
    cy.get(':nth-child(2) > .dropdown-item').click() //Clica em frequencia
    cy.get('.navbar-toggler').click() //clica na navbar
    cy.get(':nth-child(4) > .nav-link').click()//clica em perfil
    cy.get('.navbar-toggler').click()//clica na navbar
    cy.get(':nth-child(5) > .nav-link').click() //clica no diario
  });


  it('Register as Student', () => {
    cy.visit('/');
    cy.get('a').click();
    cy.get('[type="text"]').type(randomName); // Usa o nome gerado
    cy.get('[type="email"]').type(randomEmail); // Usa o email gerado
    cy.get(':nth-child(3) > .form-control').type('123');
    cy.get('#user-type').select('aluno'); // Define o tipo como 'collector'
    cy.get('.btn').click();
    cy.visit('');
    cy.get(':nth-child(2) > .form-control').type(randomName); // Reutiliza o mesmo nome
    cy.get(':nth-child(3) > .form-control').type('123');
    cy.get('.btn').click();
    //Dentro da página do coletor

  });
});
