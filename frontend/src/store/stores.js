import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isLoading: false,
      error: null,

      setUser: (user) => set({ user }),
      setAccessToken: (token) => set({ accessToken: token }),
      setRefreshToken: (token) => set({ refreshToken: token }),
      setLoading: (loading) => set({ isLoading: loading }),
      setError: (error) => set({ error }),

      logout: () => set({
        user: null,
        accessToken: null,
        refreshToken: null,
        error: null
      }),

      isAuthenticated: () => !!get().accessToken,
      getUser: () => get().user
    }),
    {
      name: 'auth-store'
    }
  )
);

export const useChatStore = create((set, get) => ({
  threads: [],
  currentThreadId: null,
  messages: [],
  isLoading: false,

  setThreads: (threads) => set({ threads }),
  setCurrentThreadId: (id) => set({ currentThreadId: id }),
  setMessages: (messages) => set({ messages }),
  setLoading: (loading) => set({ isLoading: loading }),

  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message]
  })),

  createNewThread: (threadId) => set((state) => ({
    threads: [{ id: threadId, created_at: new Date() }, ...state.threads],
    currentThreadId: threadId,
    messages: []
  }))
}));

export const useResumeStore = create((set) => ({
  resume: null,
  analysis: null,
  skillGaps: null,
  isLoading: false,

  setResume: (resume) => set({ resume }),
  setAnalysis: (analysis) => set({ analysis }),
  setSkillGaps: (gaps) => set({ skillGaps: gaps }),
  setLoading: (loading) => set({ isLoading: loading }),

  clearResume: () => set({
    resume: null,
    analysis: null,
    skillGaps: null
  })
}));
