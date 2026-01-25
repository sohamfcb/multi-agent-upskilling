import React from 'react';
import { motion } from 'framer-motion';

const Card = ({ children, className = '', ...props }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    className={`
      bg-gradient-to-br from-slate-800 to-slate-900 
      border border-slate-700 rounded-xl p-6
      shadow-lg hover:shadow-xl transition-shadow duration-300
      ${className}
    `}
    {...props}
  >
    {children}
  </motion.div>
);

export default Card;
