const username = `user_${Date.now()}`
const password = 'secret'

function login() {
  cy.visit('/login')
  cy.get('input[placeholder="Username"]').type(username)
  cy.get('input[type="password"]').type(password)
  cy.contains('button', 'Login').click()
  cy.url().should('include', '/projects')
}

describe('App E2E', () => {
  it('registers a new user', () => {
    cy.visit('/register')
    cy.get('input[placeholder="Username"]').type(username)
    cy.get('input[type="password"]').type(password)
    cy.contains('button', 'Register').click()
    cy.url().should('include', '/projects')
  })

  it('logs in and creates a project', () => {
    login()
    cy.window().then(win => {
      const token = win.localStorage.getItem('token')
      cy.request({
        method: 'POST',
        url: 'http://localhost:8000/projects/',
        qs: { token },
        body: { label: 'Test Project' },
      }).then(r => {
        expect(r.status).to.eq(200)
        win.sessionStorage.setItem('projectId', r.body.id)
      })
    })
  })

  it('adds a document and shows preview', () => {
    login()
    cy.window().then(win => {
      const token = win.localStorage.getItem('token')
      const projectId = win.sessionStorage.getItem('projectId')
      cy.request({
        method: 'POST',
        url: 'http://localhost:8000/documents/',
        qs: { token },
        body: { text: '# Hello', project_id: projectId },
      }).then(r => {
        expect(r.status).to.eq(200)
        const docId = r.body.id
        cy.visit(`/project/${projectId}/documents/${docId}`)
        cy.contains('h1', 'Hello')
      })
    })
  })
})
