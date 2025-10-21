import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiRequest } from '../api'

export default function CourseDetailPage({ token }) {
  const { id } = useParams()
  const [course, setCourse] = useState(null)

  useEffect(() => {
    apiRequest(`/courses/${id}`).then(setCourse)
  }, [id])

  if (!course) return <p>Loading...</p>

  return (
    <div style={{ padding: 20}}>
      <h2>{course.title}</h2>
      <p>{course.description}</p>
      <h3>Lessons</h3>
      {course.lessons?.map(l => (
        <div key={l.id}>
          <strong>{l.title}</strong>
          {l.tasks?.map(t => (
            <div key={t.id}>
              <Link to={`/tasks/${t.id}`}>{t.title}</Link> — {t.status}
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}
