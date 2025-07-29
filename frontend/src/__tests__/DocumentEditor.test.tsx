import { renderSanitizedMarkdown } from '../pages/DocumentEditor'

test('sanitizes malicious html', () => {
  const html = renderSanitizedMarkdown('<img src=x onerror="alert(1)"><script>alert(1)</script>')
  expect(html).not.toMatch(/<script>/)
  expect(html).not.toMatch(/<img/)
})
