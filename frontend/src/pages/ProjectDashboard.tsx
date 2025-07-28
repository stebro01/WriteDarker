import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api'
import { useAuth } from '../AuthContext'

interface Project { id: number; label: string; description?: string }
interface Document { id: number; label?: string }

export default function ProjectDashboard() {
  const { id } = useParams()
  const { token } = useAuth()
  const [project, setProject] = useState<Project | null>(null)
  const [documents, setDocuments] = useState<Document[]>([])

  useEffect(() => {
    if (!token || !id) return
    api.get(`/projects/${id}`, { params: { token } }).then(r => setProject(r.data))
    api.get(`/documents/project/${id}`, { params: { token } }).then(r => setDocuments(r.data))
  }, [token, id])

  if (!project) return <div className="p-4">Loading...</div>

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl mb-4">{project.label}</h1>
      <p className="mb-4">{project.description}</p>
      <h2 className="text-xl mb-2">Documents</h2>
      <ul className="space-y-2">
        {documents.map(d => (
          <li key={d.id} className="border p-2">
            <Link to={`/project/${id}/documents/${d.id}`}>{d.label || 'Untitled'}</Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
