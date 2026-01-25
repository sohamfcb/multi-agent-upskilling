import React from 'react';
import { motion } from 'framer-motion';

const Input = React.forwardRef(({
  label,
  error,
  icon: Icon = null,
  type = 'text',
  className = '',
  ...props
}, ref) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full"
    >
      {label && (
        <label className="block text-sm font-medium text-slate-300 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <Icon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
        )}
        <input
          ref={ref}
          type={type}
          className={`
            w-full px-4 py-2.5 rounded-lg
            bg-slate-800 border-2 border-slate-700 text-white placeholder-slate-400
            focus:outline-none focus:border-blue-500 focus:bg-slate-800/80
            transition-all duration-200
            ${Icon ? 'pl-10' : ''}
            ${error ? 'border-red-500 bg-red-900/10' : ''}
            ${className}
          `}
          {...props}
        />
      </div>
      {error && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-red-400 text-sm mt-1"
        >
          {error}
        </motion.p>
      )}
    </motion.div>
  );
});

Input.displayName = 'Input';

export default Input;
