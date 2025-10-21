import React, { useState, useEffect } from 'react'
import { apiRequest } from '../../api'
import '../../index.css'

export default function UserPage({ token }) {
  const [users, setUsers] = useState([])
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('user')

  const loadUsers = async () => {
    const data = await apiRequest('/admin/users', 'GET', null, token)
    setUsers(data || [])
  }

  const createUser = async () => {
    if (!username || !password) return alert('Введите имя пользователя и пароль!')
    await apiRequest(`/admin/users?username=${username}&password=${password}&role=${role}`, 'POST', null, token)
    setUsername('')
    setPassword('')
    setRole('user')
    await loadUsers()
  }

  const deleteUser = async (id) => {
    if (!window.confirm('Удалить пользователя?')) return
    await apiRequest(`/admin/users/${id}`, 'DELETE', null, token)
    await loadUsers()
  }

  useEffect(() => { loadUsers() }, [])

  return (
    <div className="cont">
      <h2 style={{ fontSize: 24, marginBottom: 16 }}>Пользователи</h2>

      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        <input
          value={username}
          onChange={e => setUsername(e.target.value)}
          placeholder="Имя пользователя"
        />
        <input
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          placeholder="Пароль"
        />
        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="user">user</option>
          <option value="admin">admin</option>
        </select>
        <button onClick={createUser}>Создать</button>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#e5e7eb' }}>
            <th style={{ textAlign: 'left', padding: 8 }}>ID</th>
            <th style={{ textAlign: 'left', padding: 8 }}>Имя пользователя</th>
            <th style={{ textAlign: 'left', padding: 8 }}>Роль</th>
            <th style={{ textAlign: 'center', padding: 8 }}>Действия</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: 8 }}>{u.id}</td>
              <td style={{ padding: 8 }}>{u.username}</td>
              <td style={{ padding: 8 }}>{u.role}</td>
              <td style={{ textAlign: 'center', padding: 8 }}>
                <button onClick={() => deleteUser(u.id)}>🗑️</button>
              </td>
            </tr>
          ))}
          {users.length === 0 && (
            <tr>
              <td colSpan="4" style={{ textAlign: 'center', padding: 12, color: '#6b7280' }}>
                Нет пользователей
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
