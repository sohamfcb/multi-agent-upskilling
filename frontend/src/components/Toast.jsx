import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

const Toast = ({
  id,
  type = 'info',
  title,
  message,
  onClose
}) => {
  const icons = {
    success: <CheckCircle className="w-5 h-5 text-green-400" />,
    error: <AlertCircle className="w-5 h-5 text-red-400" />,
    info: <Info className="w-5 h-5 text-blue-400" />
  };

  const bgColors = {
    success: 'bg-gradient-to-r from-green-900/50 to-green-800/50 border-green-700',
    error: 'bg-gradient-to-r from-red-900/50 to-red-800/50 border-red-700',
    info: 'bg-gradient-to-r from-blue-900/50 to-blue-800/50 border-blue-700'
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 100 }}
      className={`${bgColors[type]} border border-opacity-50 rounded-lg p-4 max-w-md`}
    >
      <div className="flex items-start gap-3">
        {icons[type]}
        <div className="flex-1">
          {title && <h3 className="font-semibold text-white mb-1">{title}</h3>}
          <p className="text-sm text-slate-300">{message}</p>
        </div>
        <button
          onClick={onClose}
          className="text-slate-400 hover:text-slate-200 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </motion.div>
  );
};

export default Toast;
