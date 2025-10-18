import React from 'react'
import { Link } from 'react-router-dom'

export default function Navbar({ token, role, onLogout }) {
  return (
    <nav style={{ padding: 10, background: '#eee' }}>
      <Link to="/courses">Courses</Link>
      {token ? (
        <>
          {role === 'admin' && <> | <Link to="/admin">Admin</Link></>}
          {' | '}<button onClick={onLogout}>Logout</button>
        </>
      ) : (
        <>
          {' | '}<Link to="/login">Login</Link>
          {' | '}<Link to="/register">Register</Link>
        </>
      )}
    </nav>
  )
}
