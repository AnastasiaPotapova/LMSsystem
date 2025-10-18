import React, { useState, useEffect } from 'react'
import { apiRequest } from '../../api'
import { Link } from 'react-router-dom';
import '../../index.css'

export default function LessonsPage({ token }) {
  const [lessons, setLessons] = useState([])
  const [chapters, setChapters] = useState([])

  const [title, setTitle] = useState('')
  const [chapterId, setChapterId] = useState('')

  const loadData = async () => {
    const chaptersData = await apiRequest('/admin/chapters', 'GET', null, token)
    setChapters(chaptersData || [])
    const lessonsData = await apiRequest('/admin/lessons', 'GET', null, token)
    setLessons(lessonsData || [])
  }

  const createLesson = async () => {
    if (!title) return alert('Введите название!')
    if (!chapterId) return alert('Выберите главу!')
    await apiRequest(`/admin/lessons?title=${title}&content=&chapter_id=${chapterId}`, 'POST', null, token)
    setTitle('')
    await loadData()
  }

  const deleteLesson = async (id) => {
    if (!window.confirm('Удалить урок?')) return
    await apiRequest(`/admin/lessons/${id}`, 'DELETE', null, token)
    await loadData()
  }

  useEffect(() => { loadData() }, [])

  return (
    <div className="cont">
      <h2 style={{ fontSize: 24, marginBottom: 16 }}>Уроки</h2>

      {/* форма создания */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Название урока"
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
        <button onClick={createLesson}>Создать</button>
      </div>

      {/* таблица уроков */}
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
          {lessons.map(l => (
            <tr key={l.id} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: 8 }}>{l.id}</td>
              <td style={{ padding: 8 }}>{l.title}</td>
              <td style={{ padding: 8 }}>
                {chapters.find(ch => ch.id === l.chapter_id)?.title || '—'}
              </td>
              <td style={{ textAlign: 'center', padding: 8 }}>
                <Link to={`/lessons/${l.id}`} className="edit-btn">
                  Редактировать
                </Link>
                <button onClick={() => deleteLesson(l.id)}>🗑️</button>
              </td>
            </tr>
          ))}
          {lessons.length === 0 && (
            <tr>
              <td
                colSpan="4"
                style={{ textAlign: 'center', padding: 12, color: '#6b7280' }}
              >
                Нет уроков
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
