import { useRef } from 'react'
import api from './api'
import { useAuth } from './AuthContext'
import DiffMatchPatch from 'diff-match-patch'

export default function usePatchSync(docId?: string, text?: string) {
  const { token } = useAuth()
  const prev = useRef(text || '')
  const dmp = useRef(new DiffMatchPatch())

  return async () => {
    if (!token || !docId) return
    const patch = dmp.current.patch_toText(dmp.current.patch_make(prev.current, text || ''))
    prev.current = text || ''
    if (patch) {
      await api.patch(`/documents/${docId}`, { patch }, { params: { token } })
    }
  }
}
