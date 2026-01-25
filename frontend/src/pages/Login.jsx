import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail, Lock, Eye, EyeOff, AlertCircle } from 'lucide-react';
import { useAuthStore } from '../store/stores';
import { authAPI } from '../services/endpoints';
import Button from '../components/Button';
import Input from '../components/Input';
import Card from '../components/Card';

const Login = () => {
  const navigate = useNavigate();
  const { setUser, setAccessToken, setRefreshToken } = useAuthStore();
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  
  const [formData, setFormData] = useState({
    identifier: '', // can be email or username
    password: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    if (!formData.identifier || !formData.password) {
      setErrors({
        submit: 'Please fill in all fields'
      });
      return;
    }

    setLoading(true);
    try {
      const loginPayload = {
        password: formData.password
      };

      // Determine if identifier is email or username
      if (formData.identifier.includes('@')) {
        loginPayload.email = formData.identifier;
      } else {
        loginPayload.username = formData.identifier;
      }

      const response = await authAPI.login(loginPayload);

      if (response.status === 200) {
        setAccessToken(response.data.access_token);
        setRefreshToken(response.data.refresh_token);
        // Note: You might want to fetch user details separately
        setUser({ username: formData.identifier });
        navigate('/dashboard');
      }
    } catch (error) {
      setErrors({
        submit: error.response?.data?.message || 'Login failed. Please try again.'
      });
    } finally {
      setLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen pt-20 pb-12 px-4 sm:px-6 flex items-center justify-center">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="w-full max-w-md"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Welcome Back
          </h1>
          <p className="text-slate-400">Sign in to your account</p>
        </motion.div>

        {/* Login Form */}
        <motion.form
          variants={itemVariants}
          onSubmit={handleSubmit}
          className="space-y-4"
        >
          <Card>
            <div className="space-y-4">
              <Input
                label="Email or Username"
                placeholder="your@email.com or username"
                icon={Mail}
                value={formData.identifier}
                onChange={(e) => setFormData({ ...formData, identifier: e.target.value })}
              />

              <div className="relative">
                <Input
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="••••••••"
                  icon={Lock}
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-10 text-slate-400 hover:text-slate-200"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>

              {errors.submit && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex items-center gap-2 text-red-400 text-sm bg-red-900/20 p-3 rounded-lg"
                >
                  <AlertCircle className="w-4 h-4" />
                  {errors.submit}
                </motion.div>
              )}

              <motion.div whileHover={{ x: 5 }} className="flex justify-end">
                <Link
                  to="/register"
                  className="text-sm text-slate-400 hover:text-slate-300 transition-colors"
                >
                  Don't have an account? Sign up
                </Link>
              </motion.div>

              <Button
                type="submit"
                variant="primary"
                size="lg"
                fullWidth
                loading={loading}
              >
                Sign In
              </Button>
            </div>
          </Card>
        </motion.form>

        {/* Demo Info */}
        <motion.div
          variants={itemVariants}
          className="mt-8 p-4 bg-slate-800/50 border border-slate-700 rounded-lg text-slate-400 text-sm"
        >
          <p className="font-semibold mb-2">Demo Credentials:</p>
          <p>Email: demo@example.com</p>
          <p>Password: demo123456</p>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Login;
