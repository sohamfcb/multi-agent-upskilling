import React from 'react';
import { motion } from 'framer-motion';

const Button = React.forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  fullWidth = false,
  icon: Icon = null,
  ...props
}, ref) => {
  const variants = {
    primary: 'bg-gradient-to-r from-slate-700 to-slate-800 hover:from-slate-600 hover:to-slate-700 text-white shadow-lg shadow-slate-900/50',
    secondary: 'bg-slate-700 hover:bg-slate-600 text-slate-50',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    ghost: 'bg-transparent hover:bg-slate-800 text-slate-300',
    outline: 'border-2 border-slate-600 bg-transparent text-slate-400 hover:bg-slate-800/50'
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <motion.button
      ref={ref}
      whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
      whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
      disabled={disabled || loading}
      className={`
        rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2
        ${variants[variant]} ${sizes[size]}
        ${fullWidth ? 'w-full' : ''}
        ${disabled || loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
      `}
      {...props}
    >
      {Icon && !loading && <Icon className="w-4 h-4" />}
      {loading && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-4 h-4 border-2 border-current border-r-transparent rounded-full"
        />
      )}
      {children}
    </motion.button>
  );
});

Button.displayName = 'Button';

export default Button;
