import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

const PageLoader = () => (
  <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
    <motion.div
      animate={{ scale: [1, 1.1, 1] }}
      transition={{ duration: 2, repeat: Infinity }}
      className="flex flex-col items-center gap-4"
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
        className="relative w-16 h-16"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg blur-lg opacity-75" />
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-700 rounded-lg flex items-center justify-center">
          <Sparkles className="w-8 h-8 text-white" />
        </div>
      </motion.div>
      <motion.p
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className="text-slate-400 text-lg"
      >
        Loading...
      </motion.p>
    </motion.div>
  </div>
);

export default PageLoader;
