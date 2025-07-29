import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
import api from '../api'
import { useAuth } from '../AuthContext'
import usePatchSync from '../usePatchSync'

const md = new MarkdownIt()

export function renderSanitizedMarkdown(text: string) {
  const html = md.render(text)
  return DOMPurify.sanitize(html)
}

export default function DocumentEditor() {
  const { id, docId } = useParams()
  const { token } = useAuth()
  const [text, setText] = useState('')
  const [refs, setRefs] = useState<any[]>([])
  const sync = usePatchSync(docId, text)

  useEffect(() => {
    if (!token || !id) return
    api.get(`/references/project/${id}`, { params: { token } }).then(r => setRefs(r.data))
  }, [token, id])

  useEffect(() => {
    if (!token || !docId) return
    api.get(`/documents/${docId}`, { params: { token } }).then(r => setText(r.data.text || ''))
  }, [token, docId])

  const save = async () => {
    await sync()
  }

  const uploadPdf = (file: File | null) => {
    if (!file || !token || !docId) return
    const fd = new FormData()
    fd.append('pdf', file)
    api.post(`/documents/${docId}/pdf`, fd, { params: { token } })
  }

  const uploadImage = (file: File | null) => {
    if (!file || !token || !docId) return
    const fd = new FormData()
    fd.append('image', file)
    api.post(`/documents/${docId}/image`, fd, { params: { token } })
  }

  const [query, setQuery] = useState('')
  const [refPdf, setRefPdf] = useState<File | null>(null)

  const [showLit, setShowLit] = useState(true)
  const [showPdfs, setShowPdfs] = useState(true)
  const [showRefs, setShowRefs] = useState(true)
  const [showMedia, setShowMedia] = useState(true)

  const addRef = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!token || !id) return
    const fd = new FormData()
    fd.append('project_id', id)
    fd.append('query', query)
    if (refPdf) fd.append('pdf', refPdf)
    const r = await api.post('/references/', fd, { params: { token } })
    setRefs([...refs, r.data])
    setQuery('')
    setRefPdf(null)
  }

  return (
    <div className="flex h-screen bg-[#1f2937] text-[#f3f4f6]">
      <div className="w-2/3 flex flex-col">
        <textarea
          className="flex-1 p-2 border"
          value={text}
          onChange={e => setText(e.target.value)}
          onBlur={save}
        />
        <div
          className="flex-1 p-2 prose prose-invert overflow-auto"
          dangerouslySetInnerHTML={{ __html: renderSanitizedMarkdown(text) }}
        />
      </div>
      <div className="w-1/3 p-2 space-y-4 overflow-auto border-l">
        <div>
          <button
            className="w-full flex justify-between items-center bg-chat-panel p-2 rounded"
            onClick={() => setShowLit(!showLit)}
          >
            <span className="font-bold">Literature</span>
            <span>{showLit ? '-' : '+'}</span>
          </button>
          {showLit && (
            <div className="mt-2 text-sm">Add notes about the literature here.</div>
          )}
        </div>

        <div>
          <button
            className="w-full flex justify-between items-center bg-chat-panel p-2 rounded"
            onClick={() => setShowPdfs(!showPdfs)}
          >
            <span className="font-bold">PDFs</span>
            <span>{showPdfs ? '-' : '+'}</span>
          </button>
          {showPdfs && (
            <div className="mt-2">
              <input type="file" accept="application/pdf" onChange={e => uploadPdf(e.target.files?.[0] || null)} />
            </div>
          )}
        </div>

        <div>
          <button
            className="w-full flex justify-between items-center bg-chat-panel p-2 rounded"
            onClick={() => setShowMedia(!showMedia)}
          >
            <span className="font-bold">Media</span>
            <span>{showMedia ? '-' : '+'}</span>
          </button>
          {showMedia && (
            <div className="mt-2">
              <input type="file" accept="image/*" onChange={e => uploadImage(e.target.files?.[0] || null)} />
            </div>
          )}
        </div>

        <div>
          <button
            className="w-full flex justify-between items-center bg-chat-panel p-2 rounded"
            onClick={() => setShowRefs(!showRefs)}
          >
            <span className="font-bold">References</span>
            <span>{showRefs ? '-' : '+'}</span>
          </button>
          {showRefs && (
            <div className="mt-2">
              <form onSubmit={addRef} className="space-y-2">
                <input className="border p-1 w-full" value={query} onChange={e => setQuery(e.target.value)} placeholder="PubMed ID" />
                <input type="file" accept="application/pdf" onChange={e => setRefPdf(e.target.files?.[0] || null)} />
                <button className="bg-blue-500 text-white px-2 py-1" type="submit">Add</button>
              </form>
              <ul className="mt-2 list-disc list-inside text-sm">
                {refs.map(r => (
                  <li key={r.id}>{r.title}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
