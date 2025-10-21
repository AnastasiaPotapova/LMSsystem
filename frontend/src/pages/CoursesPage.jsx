import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiRequest } from '../api';
import '../index.css'; // отдельный CSS-файл для карточек

export default function CoursesPage({ token }) {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    apiRequest('/courses').then(setCourses);
  }, []);

  const enroll = async (id) => {
    await apiRequest(`/courses/${id}/enroll`, 'POST', null, token);
    alert('Enrolled!');
  };

  return (
    <div className="courses-container">
      {courses.map(c => (
        <div key={c.id} className="course-card">
          <h3 className="course-title">{c.title}</h3>
          <p className="course-description">{c.description}</p>
          {token && <button className="enroll-btn" onClick={() => enroll(c.id)}>Enroll</button>}
        </div>
      ))}
    </div>
  );
}
