import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { apiRequest } from '../api';
import '../TaskPage.css';
import { useParams } from 'react-router-dom';

export default function TaskPage({ token }) {
  const { id } = useParams();
  const [task, setTask] = useState({ title: '', content: '' });
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState('');

  useEffect(() => {
    if (!token) return;
    apiRequest(`/tasks/${id}`, 'GET', null, token).then(data => {
      setTask(data);
      setDraft(data.content);
    });
  }, [id, token]);

  const save = async () => {
    await apiRequest(`/tasks/${id}`, 'PUT', { content: draft }, token);
    setTask({ ...task, content: draft });
    setEditing(false);
    alert('Сохранено!');
  };

  return (
    <div className="task-page">
      <h2>{task.title}</h2>

      {editing ? (
        <div className="task-editor">
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
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {task.content}
          </ReactMarkdown>
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
