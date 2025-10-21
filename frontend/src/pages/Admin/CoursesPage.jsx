import React, { useState, useEffect } from 'react'
import { apiRequest } from '../../api'
import '../../index.css'

export default function CoursesPage({ token }) {
  const [courses, setCourses] = useState([])
  const [title, setTitle] = useState('')
  const [desc, setDesc] = useState('')

  const loadCourses = async () => {
    const data = await apiRequest('/admin/courses', 'GET', null, token)
    setCourses(data || [])
  }

  const createCourse = async () => {
    if (!title) return alert('Введите название!')
    await apiRequest(`/admin/courses?title=${title}&description=${desc}`, 'POST', null, token)
    setTitle('')
    setDesc('')
    await loadCourses()
  }

  const deleteCourse = async (id) => {
    if (!window.confirm('Удалить курс?')) return
    await apiRequest(`/admin/courses/${id}`, 'DELETE', null, token)
    await loadCourses()
  }

  useEffect(() => { loadCourses() }, [])

  return (
    <div className="cont">
      <h2 style={{ fontSize: 24, marginBottom: 16 }}>Курсы</h2>

      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Название курса" />
        <input value={desc} onChange={e => setDesc(e.target.value)} placeholder="Описание" />
        <button onClick={createCourse}>Создать</button>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#e5e7eb' }}>
            <th style={{ textAlign: 'left', padding: 8 }}>ID</th>
            <th style={{ textAlign: 'left', padding: 8 }}>Название</th>
            <th style={{ textAlign: 'left', padding: 8 }}>Описание</th>
            <th style={{ textAlign: 'center', padding: 8 }}>Действия</th>
          </tr>
        </thead>
        <tbody>
          {courses.map(c => (
            <tr key={c.id} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: 8 }}>{c.id}</td>
              <td style={{ padding: 8 }}>{c.title}</td>
              <td style={{ padding: 8 }}>{c.description}</td>
              <td style={{ textAlign: 'center', padding: 8 }}>
                <button style={{ marginRight: 10 }} onClick={() => alert('Редактировать пока не реализовано')}>✏️</button>
                <button onClick={() => deleteCourse(c.id)}>🗑️</button>
              </td>
            </tr>
          ))}
          {courses.length === 0 && (
            <tr><td colSpan="4" style={{ textAlign: 'center', padding: 12, color: '#6b7280' }}>Нет курсов</td></tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
