import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'
import { useAuth } from '../AuthContext'

interface Project { id: number; label: string; description?: string }

export default function ProjectsPage() {
  const { token } = useAuth()
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    if (!token) return
    api.get('/projects/', { params: { token } }).then(r => setProjects(r.data))
  }, [token])

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl mb-4">Projects</h1>
      <ul className="space-y-2">
        {projects.map(p => (
          <li key={p.id} className="border p-2">
            <Link to={`/project/${p.id}`}>{p.label}</Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
