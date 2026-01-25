import axiosInstance from './api';

// Auth endpoints
export const authAPI = {
  register: (data) => axiosInstance.post('/auth/register', data),
  verifySignUp: (data) => axiosInstance.post('/auth/verify-signup', data),
  login: (data) => axiosInstance.post('/auth/login', data),
  refresh: (refreshToken) => axiosInstance.post('/auth/refresh', { refresh_token: refreshToken }),
  logout: () => axiosInstance.post('/auth/logout'),
  updateUsername: (data) => axiosInstance.put('/auth/update-username', data),
  updatePassword: (data) => axiosInstance.put('/auth/update-password', data)
};

// Chatbot endpoints
export const chatbotAPI = {
  sendMessage: (message, threadId) => 
    axiosInstance.post('/core/get-response', { message, thread_id: threadId }, {
      responseType: 'stream'
    }),
  getChatHistory: (threadId) => 
    axiosInstance.get('/core/chat-history', { params: { thread_id: threadId } }),
  getAllThreads: () => 
    axiosInstance.get('/core/all_threads')
};

// Resume endpoints
export const resumeAPI = {
  uploadResume: (file) => {
    const formData = new FormData();
    formData.append('resume', file);
    return axiosInstance.post('/core/read-resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  analyzResume: (text) => 
    axiosInstance.post('/core/analyze-resume', { resume_text: text }),
  getSkillGaps: (resumeText, jobDescription) =>
    axiosInstance.post('/core/skill-gaps', { resume_text: resumeText, job_description: jobDescription })
};

export default {
  authAPI,
  chatbotAPI,
  resumeAPI
};
