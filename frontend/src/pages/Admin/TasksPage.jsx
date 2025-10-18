import React, { useState, useEffect } from 'react'
import { apiRequest } from '../../api'
import '../../index.css'
import { Link } from 'react-router-dom';

export default function TasksPage({ token }) {
  const [tasks, setTasks] = useState([])
  const [chapters, setChapters] = useState([])

  const [title, setTitle] = useState('')
  const [chapterId, setChapterId] = useState('')

  const loadData = async () => {
    const chaptersData = await apiRequest('/admin/chapters', 'GET', null, token)
    setChapters(chaptersData || [])
    const tasksData = await apiRequest('/admin/tasks', 'GET', null, token)
    setTasks(tasksData || [])
  }

  const createTask = async () => {
    if (!title) return alert('Введите название!')
    if (!chapterId) return alert('Выберите главу!')
    await apiRequest(
      `/admin/tasks`,
      'POST',
      { title, description: '', chapter_id: chapterId },
      token
    )

    setTitle('')
    await loadData()
  }

  const deleteTask = async (id) => {
    if (!window.confirm('Удалить задание?')) return
    await apiRequest(`/admin/tasks/${id}`, 'DELETE', null, token)
    await loadData()
  }

  useEffect(() => { loadData() }, [])

  return (
    <div className="cont">
      <h2 style={{ fontSize: 24, marginBottom: 16 }}>Задания</h2>

      {/* форма создания */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Название задания"
        />
        <select
          value={chapterId}
          onChange={e => setChapterId(e.target.value)}
        >
          <option value="">Выберите главу</option>
          {chapters.map(ch => (
            <option key={ch.id} value={ch.id}>
              {ch.title}
            </option>
          ))}
        </select>
        <button onClick={createTask}>Создать</button>
      </div>

      {/* таблица заданий */}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#e5e7eb' }}>
            <th style={{ textAlign: 'left', padding: 8 }}>ID</th>
            <th style={{ textAlign: 'left', padding: 8 }}>Название</th>
            <th style={{ textAlign: 'left', padding: 8 }}>Глава</th>
            <th style={{ textAlign: 'center', padding: 8 }}>Действия</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map(t => (
            <tr key={t.id} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: 8 }}>{t.id}</td>
              <td style={{ padding: 8 }}>{t.title}</td>
              <td style={{ padding: 8 }}>
                {chapters.find(ch => ch.id === t.chapter_id)?.title || '—'}
              </td>
              <td style={{ textAlign: 'center', padding: 8 }}>
                <Link to={`/tasks/${t.id}`} className="edit-btn">
                  Редактировать
                </Link>
                <button onClick={() => deleteTask(t.id)}>🗑️</button>
              </td>
            </tr>
          ))}
          {tasks.length === 0 && (
            <tr>
              <td
                colSpan="4"
                style={{ textAlign: 'center', padding: 12, color: '#6b7280' }}
              >
                Нет заданий
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
