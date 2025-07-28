import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import MarkdownIt from 'markdown-it'
import api from '../api'
import { useAuth } from '../AuthContext'

const md = new MarkdownIt()

export default function DocumentEditor() {
  const { id, docId } = useParams()
  const { token } = useAuth()
  const [text, setText] = useState('')

  useEffect(() => {
    if (!token || !docId) return
    api.get(`/documents/${docId}`, { params: { token } }).then(r => setText(r.data.text || ''))
  }, [token, docId])

  const save = () => {
    if (!token || !docId) return
    api.put(`/documents/${docId}`, { text }, { params: { token } })
  }

  return (
    <div className="flex h-screen">
      <textarea className="w-1/2 p-2 border" value={text} onChange={e => setText(e.target.value)} onBlur={save} />
      <div className="w-1/2 p-2 prose prose-invert overflow-auto" dangerouslySetInnerHTML={{ __html: md.render(text) }} />
    </div>
  )
}
