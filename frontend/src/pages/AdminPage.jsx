import React, { useState, useEffect } from 'react'
import { useMatch } from 'react-router-dom';
import CoursesPage from './Admin/CoursesPage.jsx'
import ChaptersPage from './Admin/ChaptersPage.jsx'
import LessonsPage from './Admin/LessonsPage.jsx'
import TasksPage from './Admin/TasksPage.jsx'
import UserPage from './Admin/UserPage.jsx'
import SubmissionsPage from './Admin/SubmissionsPage.jsx'

export default function AdminPage({ token }) {
  const [active, setActive] = useState('courses')
  const match = useMatch('/admin/*'); // ловим всё, что после /admin/
  const pathSuffix = match?.pathname.split('/')[2] || 'courses'; // 'courses' по умолчанию

  const menu = [
    { key: 'courses', label: '📓 Курсы' },
    { key: 'chapters', label: '📃 Главы' },
    { key: 'lessons', label: '📖 Уроки' },
    { key: 'tasks', label: '📝 Задания' },
    { key: 'users', label: '👯‍♀️ Пользователи' },
    { key: 'Submissions', label: '📍 Решения' },
  ]

  const renderPage = () => {
    switch (pathSuffix) {
      case 'courses': return <CoursesPage token={token} />
      case 'chapters': return <ChaptersPage token={token} />
      case 'lessons': return <LessonsPage token={token} />
      case 'tasks': return <TasksPage token={token} />
      case 'users': return <UserPage token={token} />
      case 'Submissions': return <SubmissionsPage token={token} />
      default: return null
    }
  }

  return (
    <div className="admin-layout">
      {renderPage()}
    </div>
  )
}
