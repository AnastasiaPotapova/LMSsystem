import React, { useState, useEffect } from 'react'
import { apiRequest } from '../../api'
import '../../index.css'

export default function ChaptersPage({ token }) {
  const [chapters, setChapters] = useState([])
  const [courses, setCourses] = useState([])

  const [title, setTitle] = useState('')
  const [courseId, setCourseId] = useState('')

  // загрузка курсов и глав
  const loadData = async () => {
    const coursesData = await apiRequest('/admin/courses', 'GET', null, token)
    setCourses(coursesData || [])
    const chaptersData = await apiRequest('/admin/chapters', 'GET', null, token)
    setChapters(chaptersData || [])
  }

  const createChapter = async () => {
    if (!title) return alert('Введите название!')
    if (!courseId) return alert('Выберите курс!')
    await apiRequest(`/admin/chapters?title=${title}&course_id=${courseId}`, 'POST', null, token)
    setTitle('')
    await loadData()
  }

  const deleteChapter = async (id) => {
    if (!window.confirm('Удалить главу?')) return
    await apiRequest(`/admin/chapters/${id}`, 'DELETE', null, token)
    await loadData()
  }

  useEffect(() => { loadData() }, [])

  return (
    <div className="cont">
      <h2 style={{ fontSize: 24, marginBottom: 16 }}>Главы</h2>

      {/* форма создания */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Название главы"
        />
        <select
          value={courseId}
          onChange={e => setCourseId(e.target.value)}
        >
          <option value="">Выберите курс</option>
          {courses.map(c => (
            <option key={c.id} value={c.id}>
              {c.title}
            </option>
          ))}
        </select>
        <button onClick={createChapter}>Создать</button>
      </div>

      {/* таблица глав */}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#e5e7eb' }}>
            <th style={{ textAlign: 'left', padding: 8 }}>ID</th>
            <th style={{ textAlign: 'left', padding: 8 }}>Название</th>
            <th style={{ textAlign: 'left', padding: 8 }}>Курс</th>
            <th style={{ textAlign: 'center', padding: 8 }}>Действия</th>
          </tr>
        </thead>
        <tbody>
          {chapters.map(ch => (
            <tr key={ch.id} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: 8 }}>{ch.id}</td>
              <td style={{ padding: 8 }}>{ch.title}</td>
              <td style={{ padding: 8 }}>
                {courses.find(c => c.id === ch.course_id)?.title || '—'}
              </td>
              <td style={{ textAlign: 'center', padding: 8 }}>
                <button
                  style={{ marginRight: 10 }}
                  onClick={() => alert('Редактировать пока не реализовано')}
                >
                  ✏️
                </button>
                <button onClick={() => deleteChapter(ch.id)}>🗑️</button>
              </td>
            </tr>
          ))}
          {chapters.length === 0 && (
            <tr>
              <td
                colSpan="4"
                style={{ textAlign: 'center', padding: 12, color: '#6b7280' }}
              >
                Нет глав
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
