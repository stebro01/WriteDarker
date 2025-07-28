import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthProvider } from '../AuthContext'
import LoginPage from '../pages/LoginPage'

test('renders login form', () => {
  render(
    <MemoryRouter>
      <AuthProvider>
        <LoginPage />
      </AuthProvider>
    </MemoryRouter>
  )
  expect(screen.getByRole('heading', { name: 'Login' })).toBeInTheDocument()
})
