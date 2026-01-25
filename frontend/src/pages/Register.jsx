import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail, Lock, User, Eye, EyeOff, CheckCircle, AlertCircle } from 'lucide-react';
import { useAuthStore } from '../store/stores';
import { authAPI } from '../services/endpoints';
import Button from '../components/Button';
import Input from '../components/Input';
import Card from '../components/Card';

const Register = () => {
  const navigate = useNavigate();
  const { setUser, setAccessToken, setRefreshToken } = useAuthStore();
  const [step, setStep] = useState(1); // 1: Register, 2: OTP Verification
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    username: '',
    password: '',
    confirmPassword: ''
  });

  const [otpData, setOtpData] = useState({
    code: '',
    email: ''
  });

  const validateForm = () => {
    const newErrors = {};
    if (!formData.first_name) newErrors.first_name = 'First name is required';
    if (!formData.last_name) newErrors.last_name = 'Last name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) 
      newErrors.email = 'Invalid email format';
    if (!formData.username) newErrors.username = 'Username is required';
    if (!formData.password) newErrors.password = 'Password is required';
    else if (formData.password.length < 8) newErrors.password = 'Password must be at least 8 characters';
    if (formData.password !== formData.confirmPassword) 
      newErrors.confirmPassword = 'Passwords do not match';
    return newErrors;
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    try {
      const response = await authAPI.register({
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        username: formData.username,
        password: formData.password
      });

      if (response.data.status) {
        setOtpData({ ...otpData, email: formData.email });
        setStep(2);
      }
    } catch (error) {
      setErrors({ submit: error.response?.data?.message || 'Registration failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    if (!otpData.code) {
      setErrors({ otp: 'OTP is required' });
      return;
    }

    setLoading(true);
    try {
      const response = await authAPI.verifySignUp({
        email: otpData.email,
        code: otpData.code
      });

      if (response.data.status) {
        setUser(response.data.data.user);
        setAccessToken(response.data.data.token.access_token);
        setRefreshToken(response.data.data.token.refresh_token);
        navigate('/dashboard');
      }
    } catch (error) {
      setErrors({ otp: error.response?.data?.message || 'Verification failed' });
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
            Join Agent
          </h1>
          <p className="text-slate-400">Create your account and get started</p>
        </motion.div>

        {step === 1 ? (
          // Registration Form
          <motion.form
            variants={itemVariants}
            onSubmit={handleRegisterSubmit}
            className="space-y-4"
          >
            <Card>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <Input
                    label="First Name"
                    placeholder="John"
                    value={formData.first_name}
                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    error={errors.first_name}
                  />
                  <Input
                    label="Last Name"
                    placeholder="Doe"
                    value={formData.last_name}
                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    error={errors.last_name}
                  />
                </div>

                <Input
                  label="Email"
                  type="email"
                  placeholder="your@email.com"
                  icon={Mail}
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  error={errors.email}
                />

                <Input
                  label="Username"
                  placeholder="johndoe123"
                  icon={User}
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  error={errors.username}
                />

                <div className="relative">
                  <Input
                    label="Password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    icon={Lock}
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    error={errors.password}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-10 text-slate-400 hover:text-slate-200"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>

                <Input
                  label="Confirm Password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="••••••••"
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  error={errors.confirmPassword}
                />

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

                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  fullWidth
                  loading={loading}
                >
                  Create Account
                </Button>
              </div>
            </Card>
          </motion.form>
        ) : (
          // OTP Verification
          <motion.form
            variants={itemVariants}
            onSubmit={handleVerifyOTP}
            className="space-y-4"
          >
            <Card>
              <div className="space-y-4">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="w-16 h-16 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-full flex items-center justify-center mx-auto"
                >
                  <CheckCircle className="w-8 h-8 text-green-400" />
                </motion.div>

                <div className="text-center">
                  <h2 className="text-2xl font-bold text-white mb-1">Verify Email</h2>
                  <p className="text-slate-400 text-sm">We sent a 6-digit code to {otpData.email}</p>
                </div>

                <Input
                  label="Verification Code"
                  placeholder="000000"
                  maxLength="6"
                  value={otpData.code}
                  onChange={(e) => setOtpData({ ...otpData, code: e.target.value.replace(/\D/g, '') })}
                  error={errors.otp}
                  className="text-center text-2xl tracking-widest"
                />

                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  fullWidth
                  loading={loading}
                >
                  Verify Code
                </Button>

                <button
                  type="button"
                  onClick={() => {
                    setStep(1);
                    setErrors({});
                  }}
                  className="w-full text-slate-400 hover:text-slate-300 text-sm transition-colors"
                >
                  Back to Registration
                </button>
              </div>
            </Card>
          </motion.form>
        )}

        {/* Footer */}
        <motion.div variants={itemVariants} className="mt-8 text-center">
          <p className="text-slate-400">
            Already have an account?{' '}
            <Link to="/login" className="text-slate-400 hover:text-slate-300 font-medium">
              Login here
            </Link>
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Register;
