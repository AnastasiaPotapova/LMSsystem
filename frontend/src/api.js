const API_URL = "http://localhost:8000"

export async function apiRequest(path, method = 'GET', data, token) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' }
  }
  if (data) opts.body = JSON.stringify(data)
  if (token) opts.headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(API_URL + path, opts)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}
