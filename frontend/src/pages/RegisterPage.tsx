import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../api'
import { useAuth } from '../AuthContext'

export default function RegisterPage() {
  const navigate = useNavigate()
  const { setToken } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.post('/auth/register', { username, password })
      const resp = await api.post('/auth/login', { username, password })
      setToken(resp.data.access_token)
      navigate('/projects')
    } catch (err) {
      setError('Registration failed')
    }
  }

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl mb-4">Register</h1>
      <form onSubmit={onSubmit} className="flex flex-col gap-2">
        <input className="border p-2" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input className="border p-2" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        {error && <p className="text-red-500">{error}</p>}
        <button className="bg-blue-500 text-white p-2" type="submit">Register</button>
      </form>
      <p className="mt-2">Already have an account? <Link to="/login" className="text-blue-500">Login</Link></p>
    </div>
  )
}
