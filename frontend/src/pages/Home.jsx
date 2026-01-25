import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Zap, MessageSquare, FileText, Sparkles } from 'lucide-react';
import Button from '../components/Button';
import Card from '../components/Card';

const Home = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Chatbot',
      description: 'Interact with intelligent AI agents for career guidance and skill development'
    },
    {
      icon: FileText,
      title: 'Resume Analysis',
      description: 'Get comprehensive feedback on your resume with skill gaps and improvements'
    },
    {
      icon: Zap,
      title: 'Performance Tracking',
      description: 'Track your progress and upskilling journey with detailed analytics'
    },
    {
      icon: MessageSquare,
      title: 'Real-time Conversations',
      description: 'Engage in natural conversations to improve your professional skills'
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Hero Section */}
      <motion.section
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative pt-32 pb-20 px-4 sm:px-6 max-w-7xl mx-auto"
      >
        {/* Gradient Background */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-slate-700/20 rounded-full blur-3xl" />
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-slate-600/20 rounded-full blur-3xl" />
        </div>

        <motion.div
          variants={itemVariants}
          className="text-center max-w-3xl mx-auto mb-12"
        >
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, type: 'spring' }}
            className="inline-block mb-6 px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-full"
          >
            <p className="text-slate-400 text-sm font-medium">Welcome to SkillSync AI</p>
          </motion.div>

          <h1 className="text-5xl sm:text-6xl font-bold mb-6 leading-tight">
            Upskill with{' '}
            <span className="bg-gradient-to-r from-slate-300 via-slate-400 to-slate-300 bg-clip-text text-transparent">
              AI-Powered Agents
            </span>
          </h1>

          <p className="text-xl text-slate-400 mb-8 leading-relaxed">
            Transform your career with intelligent AI agents that provide personalized coaching, 
            resume analysis, and skill development guidance.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button size="lg" icon={ArrowRight}>
                Get Started Free
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline">
                Sign In
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* Feature Cards */}
        <motion.div
          variants={containerVariants}
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-20"
        >
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div key={index} variants={itemVariants}>
                <Card className="group hover:border-slate-600/50 h-full">
                  <motion.div
                    whileHover={{ rotate: 360 }}
                    transition={{ duration: 0.6 }}
                    className="w-12 h-12 bg-gradient-to-br from-slate-600/20 to-slate-700/20 rounded-lg flex items-center justify-center mb-4 group-hover:from-slate-600/40 group-hover:to-slate-700/40 transition-all"
                  >
                    <Icon className="w-6 h-6 text-slate-300" />
                  </motion.div>
                  <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{feature.description}</p>
                </Card>
              </motion.div>
            );
          })}
        </motion.div>
      </motion.section>

      {/* CTA Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="py-20 px-4 sm:px-6"
      >
        <div className="max-w-2xl mx-auto text-center">
          <Card className="bg-gradient-to-r from-slate-800 to-slate-900 border-slate-700">
            <h2 className="text-3xl font-bold text-white mb-4">Ready to Transform Your Career?</h2>
            <p className="text-slate-300 mb-6">
              Join thousands of professionals using our AI-powered platform for career advancement.
            </p>
            <Link to="/register">
              <Button size="lg" fullWidth>
                Start Your Journey
              </Button>
            </Link>
          </Card>
        </div>
      </motion.section>
    </div>
  );
};

export default Home;
