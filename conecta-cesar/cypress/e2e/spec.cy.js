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


  it('Register as Admin', () => {
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


    //Dentro da página do admin
 
  });


  it('Register as Collector', () => {
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
    cy.get('p > .btn')
    cy.get('#localizacao_atual').type(randomAdress)
    cy.get('.mt-3 > .btn').click()

  });
});