describe('Reference Upload', () => {
  beforeEach(() => {
    // Create a test user and login
    cy.request('POST', 'http://localhost:8000/auth/register', {
      username: 'cypresstest',
      password: 'testpass123'
    }).then(() => {
      cy.request('POST', 'http://localhost:8000/auth/login', {
        username: 'cypresstest', 
        password: 'testpass123'
      }).then((response) => {
        window.localStorage.setItem('auth_token', response.body.access_token)
      })
    })
  })

  it('should upload a PDF file from the Library page', () => {
    cy.visit('http://localhost:9000/library')
    
    // Wait for the page to load and check we're logged in
    cy.contains('Reference Library').should('be.visible')
    
    // Click the Upload button
    cy.contains('Upload').click()
    
    // Intercept the upload request
    cy.intercept('POST', '**/references/**').as('uploadRequest')
    
    // Upload a test file (you'll need to place a small PDF in cypress/fixtures/)
    cy.get('input[type="file"]').selectFile('cypress/fixtures/test.pdf', { force: true })
    
    // Wait for the upload to complete
    cy.wait('@uploadRequest').then((interception) => {
      expect(interception.response.statusCode).to.equal(200)
    })
    
    // Verify the file appears in the library
    cy.contains('test.pdf').should('be.visible')
  })

  it('should detect duplicate files and show error', () => {
    cy.visit('http://localhost:9000/library')
    
    // Upload first file
    cy.contains('Upload').click()
    cy.intercept('POST', '**/references/**').as('uploadRequest1')
    cy.get('input[type="file"]').selectFile('cypress/fixtures/test.pdf', { force: true })
    cy.wait('@uploadRequest1')
    
    // Try to upload the same file again
    cy.contains('Upload').click()
    cy.intercept('POST', '**/references/**').as('uploadRequest2')
    cy.get('input[type="file"]').selectFile('cypress/fixtures/test.pdf', { force: true })
    
    cy.wait('@uploadRequest2').then((interception) => {
      expect(interception.response.statusCode).to.equal(409) // Conflict - duplicate file
    })
    
    // Should show duplicate error message
    cy.on('window:alert', (text) => {
      expect(text).to.contain('already exists')
    })
  })

  it('should preview files when clicking on them', () => {
    cy.visit('http://localhost:9000/library')
    
    // Upload a file
    cy.contains('Upload').click()
    cy.intercept('POST', '**/references/**').as('uploadRequest')
    cy.get('input[type="file"]').selectFile('cypress/fixtures/test.pdf', { force: true })
    cy.wait('@uploadRequest')
    
    // Should show preview badge
    cy.contains('Preview').should('be.visible')
    
    // Click on title to preview
    cy.intercept('GET', '**/references/*/file**').as('previewRequest')
    cy.get('table tbody tr').first().find('td').first().find('button').click()
    
    // Should open preview modal
    cy.get('[role="dialog"], .fixed.inset-0').should('be.visible')
    cy.contains('Preview').should('be.visible')
    
    // Should show file content (for PDF, iframe should be present)
    cy.get('iframe').should('be.visible')
    
    // Close preview
    cy.contains('Close').click()
    cy.get('[role="dialog"], .fixed.inset-0').should('not.exist')
  })

  it('should upload a PDF file from the Dashboard page', () => {
    cy.visit('http://localhost:9000/dashboard')
    
    // Wait for the page to load
    cy.contains('Welcome back').should('be.visible')
    
    // Click the Upload References button
    cy.contains('Upload References').click()
    
    // Intercept the upload request
    cy.intercept('POST', '**/references/**').as('uploadRequest')
    
    // Upload a test file
    cy.get('input[type="file"]').selectFile('cypress/fixtures/test.pdf', { force: true })
    
    // Wait for the upload to complete
    cy.wait('@uploadRequest').then((interception) => {
      expect(interception.response.statusCode).to.equal(200)
    })
    
    // Navigate to library to verify the file was uploaded
    cy.visit('http://localhost:9000/library')
    cy.contains('test.pdf').should('be.visible')
  })

  afterEach(() => {
    // Clean up: delete the test user's references
    cy.window().then((win) => {
      const token = win.localStorage.getItem('auth_token')
      if (token) {
        cy.request({
          method: 'GET',
          url: `http://localhost:8000/references/user?token=${token}`
        }).then((response) => {
          response.body.forEach((ref) => {
            cy.request('DELETE', `http://localhost:8000/references/${ref.id}?token=${token}`)
          })
        })
      }
    })
    
    // Clear localStorage
    cy.clearLocalStorage()
  })
})