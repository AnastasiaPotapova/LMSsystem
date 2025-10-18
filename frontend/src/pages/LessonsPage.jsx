import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiRequest } from '../api';
import '../LessonsPage.css';

export default function LessonsPage({ token , role}) {
  const [lessons, setLessons] = useState([]);

  useEffect(() => {
    apiRequest('/lessons').then(setLessons);
  }, []);
  return (
    <div className="lessons-page">
      <h2>Все уроки</h2>
      <ul className="lessons-list">
        {lessons.map(lesson => (
          <li key={lesson.id} className="lesson-item">
            <div className="lesson-info">
              <h3>{lesson.title}</h3>
              <p>{lesson.description || lesson.content.slice(0, 100) + '...'}</p>
            </div>
            <div className="lesson-actions">
              <Link to={`/lessons/${lesson.id}`} className="open-btn">
                Открыть
              </Link>

            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
