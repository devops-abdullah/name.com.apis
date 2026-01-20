import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FiMenu, FiX, FiLogOut, FiHome, FiUsers, FiSettings } from 'react-icons/fi'
import '../styles/navbar.css'

const Navbar: React.FC = () => {
  const [menuOpen, setMenuOpen] = useState(false)
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <h2>DNS Manager</h2>
        </div>

        <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
          {menuOpen ? <FiX /> : <FiMenu />}
        </button>

        <ul className={`navbar-menu ${menuOpen ? 'open' : ''}`}>
          <li>
            <a href="/dashboard" onClick={() => setMenuOpen(false)}>
              <FiHome /> Dashboard
            </a>
          </li>
          <li>
            <a href="/teams" onClick={() => setMenuOpen(false)}>
              <FiUsers /> Teams
            </a>
          </li>
          <li>
            <a href="/settings" onClick={() => setMenuOpen(false)}>
              <FiSettings /> Settings
            </a>
          </li>
          <li>
            <button className="btn btn-secondary" onClick={handleLogout}>
              <FiLogOut /> Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  )
}

export default Navbar
