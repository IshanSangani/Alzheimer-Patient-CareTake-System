import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const NavBar = () => {
  const navigate = useNavigate();
  const notificationCount = 2;

  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-white w-full shadow-sm">
      <div className="flex items-center gap-2 text-2xl font-bold cursor-pointer" onClick={() => navigate('/')}>CareConnect <span className="text-blue-600">AI</span></div>
      <div className="flex items-center gap-8 text-lg font-medium">
        <Link to="/" className="flex items-center gap-1 hover:text-blue-600 transition-colors">
          <span className="material-icons">Home</span> 
        </Link>
        <Link to="/dashboard" className="flex items-center gap-1 hover:text-blue-600 transition-colors relative">
          <span className="material-icons">Dashboard</span>
          {notificationCount > 0 && (
            <span className="absolute -top-2 -right-4 bg-blue-600 text-white text-xs rounded-full px-2">{notificationCount}</span>
          )}
        </Link>
        <Link to="/profile" className="flex items-center gap-1 hover:text-blue-600 transition-colors">
          <span className="material-icons">Profile</span>
        </Link>
        <Link to="/device" className="flex items-center gap-1 hover:text-blue-600 transition-colors">
          <span className="material-icons">Device Settings</span>
        </Link>
        <Link to="/about" className="flex items-center gap-1 hover:text-blue-600 transition-colors">
          <span className="material-icons">About</span>
        </Link>
        <Link to="/contact" className="flex items-center gap-1 hover:text-blue-600 transition-colors">
          <span className="material-icons">Contact</span>
        </Link>
        <button className="ml-2 hover:text-blue-600 transition-colors" aria-label="Notifications">
          <span className="material-icons">Notifications</span>
        </button>
      </div>
    </nav>
  );
};

export default NavBar;
