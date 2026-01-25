import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Menu, X, LogOut, User, Settings } from 'lucide-react';
import { useAuthStore } from '../store/stores';

const Navbar = () => {
  const [isOpen, setIsOpen] = React.useState(false);
  const location = useLocation();
  const { user, logout } = useAuthStore();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated());

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard', protected: true },
    { name: 'Chatbot', path: '/chat', protected: true },
    { name: 'Resume Analyzer', path: '/resume', protected: true }
  ];

  const visibleLinks = isAuthenticated 
    ? navLinks
    : navLinks.filter(link => !link.protected);

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-slate-950 to-slate-900 backdrop-blur-md border-b border-slate-800"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <motion.div
              whileHover={{ scale: 1.1 }}
              className="w-8 h-8 bg-gradient-to-br from-slate-700 to-slate-900 rounded-lg flex items-center justify-center border border-slate-600"
            >
              <span className="text-white font-bold text-sm">SA</span>
            </motion.div>
            <span className="text-xl font-bold text-white">
              SkillSync AI
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {visibleLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-2 rounded-lg transition-all duration-200 ${
                  location.pathname === link.path
                    ? 'bg-slate-700 text-white'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                {link.name}
              </Link>
            ))}
          </div>

          {/* User Menu / Auth Buttons */}
          <div className="hidden md:flex items-center gap-4">
            {isAuthenticated ? (
              <div className="flex items-center gap-4">
                <div className="text-sm">
                  <p className="text-slate-300">Welcome,</p>
                  <p className="font-semibold text-white">{user?.username}</p>
                </div>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={logout}
                  className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
                >
                  <LogOut className="w-5 h-5 text-slate-300" />
                </motion.button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link
                  to="/login"
                  className="px-4 py-2 text-slate-400 hover:text-white transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2.5 bg-gradient-to-r from-slate-700 to-slate-800 text-white rounded-lg hover:shadow-lg hover:shadow-slate-600/20 hover:from-slate-600 hover:to-slate-700 transition-all"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 hover:bg-slate-700 rounded-lg transition-colors"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden pb-4 space-y-2"
          >
            {visibleLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setIsOpen(false)}
                className="block px-4 py-2 text-slate-300 hover:bg-slate-700 rounded-lg transition-colors"
              >
                {link.name}
              </Link>
            ))}
            {!isAuthenticated && (
              <>
                <Link
                  to="/login"
                  className="block px-4 py-2 text-slate-300 hover:bg-slate-700 rounded-lg transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Sign Up
                </Link>
              </>
            )}
          </motion.div>
        )}
      </div>
    </motion.nav>
  );
};

export default Navbar;
