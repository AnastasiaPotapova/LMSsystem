import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { apiRequest } from '../api';
import '../LessonPage.css';
import { useParams, Link } from 'react-router-dom'

export default function LessonPage({ lesson_id, token }) {
  const { id } = useParams()
  const [lesson, setLesson] = useState({ title: '', content: '' });
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState('');

  useEffect(() => {
      if (!token) return;
      apiRequest(`/lessons/${id}`, 'GET', null, token).then(data => {
        setLesson(data);
        setDraft(data.content);
      });
  }, [id, token]);


  const save = async () => {
    await apiRequest(`/lessons/${id}`, 'PUT', { content: draft }, token);
    setLesson({ ...lesson, content: draft });
    setEditing(false);
    alert('Сохранено!');
  };

  return (
    <div className="lesson-page">
      <h2>{lesson.title}</h2>

      {editing ? (
        <div className="lesson-editor">
          <textarea
            value={draft}
            onChange={e => setDraft(e.target.value)}
            placeholder="Введите Markdown..."
          />
          <div className="editor-buttons">
            <button onClick={save}>Сохранить</button>
            <button onClick={() => setEditing(false)}>Отмена</button>
          </div>
        </div>
      ) : (
        <>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{lesson.content}</ReactMarkdown>
          {token && (
            <button className="edit-btn" onClick={() => setEditing(true)}>
              Редактировать
            </button>
          )}
        </>
      )}
    </div>
  );
}
