import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar.jsx';
import Sidebar from './components/Sidebar.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import CoursesPage from './pages/CoursesPage.jsx';
import LessonsPage from './pages/LessonsPage.jsx';
import TasksPage from './pages/TasksPage.jsx';
import LessonPage from './pages/LessonPage.jsx';
import CourseDetailPage from './pages/CourseDetailPage.jsx';
import TaskPage from './pages/TaskPage.jsx';
import AdminPage from './pages/AdminPage.jsx';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [role, setRole] = useState(localStorage.getItem('role'));
  const [isOpen, setIsOpen] = useState(window.innerWidth >= 768);

  const handleLogin = (t, r) => {
    localStorage.setItem('token', t);
    localStorage.setItem('role', r);
    setToken(t);
    setRole(r);
  };

  const handleLogout = () => {
    localStorage.clear();
    setToken(null);
    setRole(null);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) setIsOpen(false);
      else setIsOpen(true);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="app-layout">
      <Navbar token={token} role={role} onLogout={handleLogout} />
      <Sidebar role={role} isOpen={isOpen} setIsOpen={setIsOpen} />
      <main className={`main-content ${isOpen ? 'sidebar-open' : 'sidebar-collapsed'}`}>
        <Routes>
          <Route path="/" element={<Navigate to={role === 'admin' ? '/admin/courses' : '/courses'} />} />
          <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/courses" element={<CoursesPage token={token} />} />
          <Route path="/lessons" element={<LessonsPage token={token} role={role}/>} />
          <Route path="/tasks" element={<TasksPage token={token} role={role}/>} />
          <Route path="/courses/:id" element={<CourseDetailPage token={token} />} />
          <Route path="/lessons/:id" element={<LessonPage token={token} />} />
          <Route path="/tasks/:id" element={<TaskPage token={token} />} />
          {role === 'admin' && <Route path="/admin/*" element={<AdminPage token={token} />} />}
        </Routes>
      </main>
    </div>
  );
}
