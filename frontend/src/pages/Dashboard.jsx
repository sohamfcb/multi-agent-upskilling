import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, Users, Clock } from 'lucide-react';
import { useAuthStore } from '../store/stores';
import Card from '../components/Card';

const Dashboard = () => {
  const user = useAuthStore((state) => state.getUser());

  const stats = [
    {
      icon: Clock,
      label: 'Total Learning Hours',
      value: '24h 30m',
      color: 'from-slate-600 to-slate-700'
    },
    {
      icon: TrendingUp,
      label: 'Skills Improved',
      value: '12',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: Users,
      label: 'Chat Interactions',
      value: '47',
      color: 'from-slate-700 to-slate-800'
    },
    {
      icon: BarChart3,
      label: 'Resume Score',
      value: '8.5/10',
      color: 'from-orange-500 to-red-500'
    }
  ];

  const recentActivities = [
    { type: 'chat', title: 'Discussed career transition', time: '2 hours ago' },
    { type: 'resume', title: 'Analyzed resume for Sr. Developer role', time: '1 day ago' },
    { type: 'chat', title: 'Skill gap analysis discussion', time: '2 days ago' }
  ];

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
    <div className="pt-24 pb-12 px-4 sm:px-6 min-h-screen">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">
            Welcome back, <span className="text-slate-300">{user?.username}</span>
          </h1>
          <p className="text-slate-400">Track your upskilling journey and progress</p>
        </motion.div>

        {/* Stats Grid */}
        <motion.div variants={containerVariants} className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <motion.div key={index} variants={itemVariants}>
                <Card className="group hover:border-slate-600/50">
                  <div className="flex items-start justify-between mb-4">
                    <div className={`p-3 rounded-lg bg-gradient-to-br ${stat.color} bg-opacity-20`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                      className="w-2 h-2 rounded-full bg-slate-400"
                    />
                  </div>
                  <p className="text-slate-400 text-sm mb-1">{stat.label}</p>
                  <p className="text-3xl font-bold text-white">{stat.value}</p>
                </Card>
              </motion.div>
            );
          })}
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Quick Links */}
          <motion.div variants={itemVariants}>
            <Card className="h-full">
              <h2 className="text-xl font-bold text-white mb-4">Quick Links</h2>
              <div className="space-y-3">
                {[
                  { icon: '💬', text: 'Start Chat Session', href: '/chat' },
                  { icon: '📄', text: 'Upload Resume', href: '/resume' },
                  { icon: '📊', text: 'View Analytics', href: '#' }
                ].map((link, idx) => (
                  <motion.a
                    key={idx}
                    href={link.href}
                    whileHover={{ x: 4 }}
                    className="flex items-center gap-3 p-3 bg-slate-800 rounded-lg hover:bg-slate-700 transition-colors cursor-pointer"
                  >
                    <span className="text-xl">{link.icon}</span>
                    <span className="text-slate-300">{link.text}</span>
                  </motion.a>
                ))}
              </div>
            </Card>
          </motion.div>

          {/* Recent Activities */}
          <motion.div variants={itemVariants} className="lg:col-span-2">
            <Card>
              <h2 className="text-xl font-bold text-white mb-4">Recent Activities</h2>
              <div className="space-y-3">
                {recentActivities.map((activity, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: idx * 0.1 }}
                    className="flex items-center gap-4 p-3 bg-slate-800 rounded-lg hover:bg-slate-700 transition-colors"
                  >
                    <div className="w-2 h-2 rounded-full bg-slate-400" />
                    <div className="flex-1">
                      <p className="text-white text-sm font-medium">{activity.title}</p>
                      <p className="text-slate-500 text-xs">{activity.time}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </Card>
          </motion.div>
        </div>

        {/* Call to Action */}
        <motion.div variants={itemVariants} className="mt-12">
          <Card className="bg-gradient-to-r from-slate-800 to-slate-900 border-slate-700 text-center py-12">
            <h3 className="text-2xl font-bold text-white mb-3">Ready to Level Up?</h3>
            <p className="text-slate-300 mb-6">
              Start a chat session with our AI agents to get personalized coaching and guidance
            </p>
            <a
              href="/chat"
              className="inline-block px-6 py-3 bg-gradient-to-r from-slate-700 to-slate-800 hover:from-slate-600 hover:to-slate-700 text-white rounded-lg font-medium transition-all hover:shadow-lg hover:shadow-slate-900/50"
            >
              Start Chat Now
            </a>
          </Card>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
