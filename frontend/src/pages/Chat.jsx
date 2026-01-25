import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Plus, MessageCircle, Loader } from 'lucide-react';
import { useChatStore } from '../store/stores';
import { chatbotAPI } from '../services/endpoints';
import Button from '../components/Button';
import Input from '../components/Input';
import Card from '../components/Card';

const Chat = () => {
  const {
    threads,
    currentThreadId,
    messages,
    isLoading,
    setThreads,
    setCurrentThreadId,
    setMessages,
    setLoading,
    addMessage,
    createNewThread
  } = useChatStore();

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with all threads
  useEffect(() => {
    fetchThreads();
  }, []);

  const fetchThreads = async () => {
    try {
      const response = await chatbotAPI.getAllThreads();
      const threadList = response.data.response.map((thread) => ({
        id: thread.values.metadata.thread_id,
        created_at: thread.created_at
      }));
      setThreads(threadList);
      
      if (threadList.length > 0 && !currentThreadId) {
        setCurrentThreadId(threadList[0].id);
        fetchChatHistory(threadList[0].id);
      }
    } catch (error) {
      console.error('Failed to fetch threads:', error);
    }
  };

  const fetchChatHistory = async (threadId) => {
    try {
      const response = await chatbotAPI.getChatHistory(threadId);
      const formattedMessages = response.data.messages?.map((msg) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp
      })) || [];
      setMessages(formattedMessages);
    } catch (error) {
      console.error('Failed to fetch chat history:', error);
    }
  };

  const handleNewChat = () => {
    const newThreadId = `thread_${Date.now()}`;
    createNewThread(newThreadId);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || !currentThreadId) return;

    const userMessage = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    addMessage(userMessage);
    setInputValue('');
    setLoading(true);

    try {
      const response = await chatbotAPI.sendMessage(inputValue, currentThreadId);
      
      // Handle streaming response
      const reader = response.data.stream?.getReader?.();
      if (reader) {
        let botMessage = {
          id: `msg_${Date.now()}`,
          role: 'assistant',
          content: '',
          timestamp: new Date().toISOString()
        };

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const chunk = new TextDecoder().decode(value);
          const lines = chunk.split('\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                botMessage.content += data.response || '';
                addMessage({ ...botMessage });
              } catch (e) {
                console.error('Error parsing streaming data:', e);
              }
            }
          }
        }
      } else {
        // Fallback for non-streaming response
        const botMessage = {
          id: `msg_${Date.now()}`,
          role: 'assistant',
          content: response.data.response || 'No response',
          timestamp: new Date().toISOString()
        };
        addMessage(botMessage);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage = {
        id: `msg_${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      addMessage(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pt-16 pb-8 h-screen flex flex-col bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="flex flex-1 overflow-hidden gap-4 max-w-7xl mx-auto w-full px-4">
        {/* Sidebar */}
        <motion.div
          initial={{ x: -300, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className="hidden md:flex flex-col w-64 bg-slate-900/50 border-r border-slate-700 rounded-lg p-4"
        >
          <Button
            variant="primary"
            size="md"
            fullWidth
            icon={Plus}
            onClick={handleNewChat}
            className="mb-4"
          >
            New Chat
          </Button>

          <div className="flex-1 overflow-y-auto space-y-2">
            {threads.map((thread) => (
              <motion.button
                key={thread.id}
                whileHover={{ x: 4 }}
                onClick={() => {
                  setCurrentThreadId(thread.id);
                  fetchChatHistory(thread.id);
                }}
                className={`w-full text-left px-3 py-2 rounded-lg transition-all ${
                  currentThreadId === thread.id
                    ? 'bg-slate-700 text-white'
                    : 'text-slate-400 hover:bg-slate-800'
                }`}
              >
                <div className="flex items-center gap-2">
                  <MessageCircle className="w-4 h-4" />
                  <span className="truncate text-sm">Chat {new Date(thread.created_at).toLocaleDateString()}</span>
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages Area */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex-1 overflow-y-auto space-y-4 mb-4"
          >
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-slate-400">
                <MessageCircle className="w-16 h-16 mb-4 opacity-50" />
                <p className="text-lg font-medium">Start a conversation</p>
                <p className="text-sm">Ask me anything about your career development!</p>
              </div>
            ) : (
              messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <Card className={`max-w-md lg:max-w-lg ${
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-slate-700 to-slate-800'
                      : 'bg-slate-800'
                  }`}>
                    <p className="text-white whitespace-pre-wrap">{message.content}</p>
                  </Card>
                </motion.div>
              ))
            )}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex justify-start"
              >
                <Card className="bg-slate-800 flex items-center gap-2">
                  <Loader className="w-4 h-4 animate-spin text-slate-400" />
                  <p className="text-slate-400">Thinking...</p>
                </Card>
              </motion.div>
            )}
            <div ref={messagesEndRef} />
          </motion.div>

          {/* Input Area */}
          <motion.form
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            onSubmit={handleSendMessage}
            className="flex gap-3"
          >
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask me anything..."
              disabled={isLoading || !currentThreadId}
              className="flex-1 px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-400 focus:outline-none focus:border-slate-600 disabled:opacity-50"
            />
            <Button
              type="submit"
              variant="primary"
              size="md"
              icon={Send}
              disabled={isLoading || !currentThreadId}
              loading={isLoading}
            />
          </motion.form>
        </div>
      </div>
    </div>
  );
};

export default Chat;
