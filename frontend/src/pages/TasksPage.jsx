import React, { useEffect, useState } from 'react'
import { apiRequest } from '../api'
import { Link } from 'react-router-dom'

export default function TasksPage({ token }) {
  const [tasks, setTasks] = useState([])

  const loadTasks = async () => {
    try {
      const data = await apiRequest('/tasks', 'GET', null, token)
      setTasks(data || [])
    } catch (e) {
      console.error('Ошибка загрузки задач:', e)
      setTasks([])
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  return (
    <div className="tasks-page">
      <h2>Задачи</h2>
      {tasks.length === 0 ? (
        <p>Нет задач</p>
      ) : (
        tasks.map(task => (
          <div key={task.id} className="task-item">
            <Link to={`/tasks/${task.id}`}>
              <h3>{task.title || 'Без названия'}</h3>
              <p>{(task.content || '').slice(0, 100)}...</p>
            </Link>
          </div>
        ))
      )}
    </div>
  )
}
