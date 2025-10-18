import React, { useState } from 'react'

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const register = async e => {
    e.preventDefault()
    const params = new URLSearchParams({ username, password })
    const res = await fetch(`http://localhost:8000/register?${params.toString()}`, { method: 'POST' })
    if (res.ok) alert('Registered successfully!')
    else alert('Error registering')
  }

  return (
    <form onSubmit={register} style={{ padding: 20 }}>
      <h2>Register</h2>
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" /><br />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" /><br />
      <button type="submit">Register</button>
    </form>
  )
}
