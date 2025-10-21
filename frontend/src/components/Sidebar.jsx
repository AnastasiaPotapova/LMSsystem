import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../index.css';

export default function Sidebar({ role, isOpen, setIsOpen }) {
  const location = useLocation();

  // Меню в зависимости от роли
  const menu = role === 'admin'
    ? [
        { key: 'courses', label: '📓 Курсы', path: '/admin/courses' },
        { key: 'chapters', label: '📃 Главы', path: '/admin/chapters' },
        { key: 'lessons', label: '📖 Уроки', path: '/admin/lessons' },
        { key: 'tasks', label: '📝 Задания', path: '/admin/tasks' },
        { key: 'users', label: '👯‍♀️ Пользователи', path: '/admin/users' },
        { key: 'Submissions', label: '📍 Решения', path: '/admin/submissions' },
      ]
    : [
        { key: 'chapters', label: '📃 Главы', path: '/courses' },
        { key: 'lessons', label: '📖 Уроки', path: '/lessons' },
        { key: 'tasks', label: '📝 Задания', path: '/tasks' },
      ];

  return (
    <aside className={`sidebar ${isOpen ? 'open' : 'collapsed'}`}>
      <button
        className="toggle-btn"
        onClick={() => setIsOpen(!isOpen)}
        title={isOpen ? 'Скрыть меню' : 'Открыть меню'}
      >
      </button>

      {isOpen && <h2 className="sidebar-title">Меню</h2>}

      {menu.map(item => {
        const active = location.pathname.startsWith(item.path);
        return (
          <Link
            key={item.key}
            to={item.path}
            className={`menu-item ${active ? 'active' : ''}`}
            title={item.label.replace(/^[^ ]+ /,'')}
          >
            {isOpen ? item.label : item.label.split(' ')[0]}
          </Link>
        );
      })}
    </aside>
  );
}
