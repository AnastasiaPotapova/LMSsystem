import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
  e.preventDefault();

  const body = new URLSearchParams();
  body.append('grant_type', 'password');  // обязательно для OAuth2PasswordRequestForm
  body.append('username', username);
  body.append('password', password);
  body.append('scope', '');              // можно пусто
  body.append('client_id', '');          // можно пусто
  body.append('client_secret', '');      // можно пусто

  const response = await fetch('http://localhost:8000/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body
  });

  if (!response.ok) {
    const err = await response.text();
    alert('Ошибка входа: ' + err);
    return;
  }

  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  localStorage.setItem('role', data.role)
  window.location.href = '/admin';
};

  return (
    <form onSubmit={handleSubmit} style={{ padding: 20 }}>
      <h2>Login</h2>
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" /><br />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" /><br />
      <button type="submit">Login</button>
    </form>
  )
}
