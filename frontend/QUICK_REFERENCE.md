# Frontend Quick Reference & Summary

## 🎯 What's Included

### ✅ Complete Frontend Stack
- **Vite** - Lightning-fast build tool
- **React 18** - Latest React with hooks
- **React Router v6** - Modern routing
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Zustand** - Lightweight state management
- **Axios** - HTTP client with interceptors

### ✅ Pages Built
1. **Home** - Landing page with features & CTAs
2. **Login** - Email/username + password auth
3. **Register** - 2-step signup with OTP verification
4. **Dashboard** - User stats, quick links, activities
5. **Chat** - Real-time chat with AI agents
6. **Resume** - Upload, analyze, and get skill gaps

### ✅ Features
- 🔐 JWT authentication with token refresh
- 🎨 Modern, sexy UI with gradients and animations
- 📱 Fully responsive design
- 🧩 Reusable component library
- 🔌 Complete API integration
- 💾 Persistent state with localStorage
- 🎯 Protected routes
- 📊 Real-time streaming responses
- 🎭 Smooth page transitions
- 🛡️ Error handling & validation

## 📁 File Structure Quick Map

```
frontend/
├── src/
│   ├── components/
│   │   ├── Button.jsx           ← Reusable button
│   │   ├── Input.jsx            ← Form input
│   │   ├── Card.jsx             ← Card container
│   │   ├── Navbar.jsx           ← Navigation bar
│   │   ├── ProtectedRoute.jsx   ← Auth guard
│   │   ├── PageLoader.jsx       ← Loading spinner
│   │   └── Toast.jsx            ← Notifications
│   ├── pages/
│   │   ├── Home.jsx             ← Landing page
│   │   ├── Login.jsx            ← Login form
│   │   ├── Register.jsx         ← Signup form
│   │   ├── Dashboard.jsx        ← User dashboard
│   │   ├── Chat.jsx             ← Chat interface
│   │   └── Resume.jsx           ← Resume analyzer
│   ├── services/
│   │   ├── api.js               ← Axios config
│   │   └── endpoints.js         ← API functions
│   ├── store/
│   │   └── stores.js            ← Zustand stores
│   ├── styles/
│   │   └── globals.css          ← Global styles
│   ├── App.jsx                  ← Main component
│   └── main.jsx                 ← Entry point
├── index.html                   ← HTML template
├── vite.config.js               ← Vite config
├── tailwind.config.js           ← Tailwind config
├── postcss.config.js            ← PostCSS config
├── package.json                 ← Dependencies
└── README.md                    ← Full docs
```

## 🚀 Getting Started (30 seconds)

```bash
cd frontend
npm install
npm run dev
# Visit http://localhost:3000
```

## 🎨 Design Highlights

### Color Scheme
- **Background**: Dark slate (`#0f172a`)
- **Primary**: Blue gradient (`#0ea5e9` → `#0284c7`)
- **Accent**: Purple (`#a855f7`)
- **Text**: Slate-50 (white text on dark)

### Key UI Elements
- Gradient buttons with hover effects
- Smooth card transitions
- Animated loading states
- Framer Motion page transitions
- Tailwind responsive grid layouts
- Custom scrollbar styling

## 📡 API Integration Map

```
Frontend                Backend
─────────────────────────────────
Login/Register  →  POST /auth/login
                   POST /auth/register
                   POST /auth/verify-signup

Chat            →  POST /core/get-response (streaming)
                   GET /core/chat-history
                   GET /core/all_threads

Resume          →  POST /core/upload-resume
                   POST /core/analyze-resume
                   POST /core/skill-gaps
```

## 🔐 Authentication at a Glance

1. **Login** → Get `access_token` + `refresh_token`
2. **Store** → Save in Zustand store + localStorage
3. **Request** → Axios interceptor adds Bearer token
4. **Expire** → 401 response triggers token refresh
5. **Retry** → Request automatically retried
6. **Logout** → Clear tokens, redirect to login

## 🧩 Component Examples

### Using Button
```jsx
<Button variant="primary" size="lg" loading={isLoading}>
  Click Me
</Button>
```

### Using Input
```jsx
<Input
  label="Email"
  type="email"
  icon={Mail}
  error={errors.email}
/>
```

### Using Protected Route
```jsx
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>
```

### Accessing Store
```jsx
const user = useAuthStore((s) => s.user);
const logout = useAuthStore((s) => s.logout);
```

## 📊 Store Actions

### Auth Store
```javascript
setUser(user)           // Set user data
setAccessToken(token)   // Set JWT token
setRefreshToken(token)  // Set refresh token
logout()                // Clear auth data
isAuthenticated()       // Check if logged in
```

### Chat Store
```javascript
setThreads(threads)     // Set chat threads
setCurrentThreadId(id)  // Select thread
setMessages(messages)   // Set chat messages
addMessage(msg)         // Add new message
createNewThread(id)     // Start new chat
```

### Resume Store
```javascript
setResume(resume)       // Set resume data
setAnalysis(analysis)   // Set analysis results
setSkillGaps(gaps)      // Set skill gaps
clearResume()           // Clear all data
```

## 🎯 Common Tasks

### Fetch Data
```javascript
const response = await chatbotAPI.getAllThreads();
console.log(response.data);
```

### Handle Form Submission
```javascript
const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const res = await authAPI.login(formData);
    // Handle success
  } catch (err) {
    setErrors({ submit: err.response?.data?.message });
  }
};
```

### Show Toast Notification
```javascript
import toast from 'react-hot-toast';

toast.success('Success!');
toast.error('Error occurred');
toast.loading('Loading...');
```

### Navigate to Page
```javascript
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();
navigate('/dashboard');
```

## 🔧 Useful Commands

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Check code quality
npm run format       # Format code with Prettier
```

## 🐛 Common Issues & Solutions

### Port 3000 already in use
→ Edit `vite.config.js` and change port to 3001

### CORS errors
→ Ensure backend has CORS enabled and correct URL

### Tokens not persisting
→ Check localStorage in DevTools, verify Zustand config

### API 401 errors
→ Check token in Network tab, verify interceptor working

### Styles not applying
→ Check Tailwind class names, verify postcss config

## 📈 Performance Tips

- Use React DevTools Profiler to find slow components
- Lazy load large components with `React.lazy()`
- Memoize expensive computations with `useMemo`
- Use `useCallback` for event handlers in lists
- Check bundle size with `npm run build`
- Enable gzip compression on server

## 📚 Key Docs

- [README.md](./README.md) - Full documentation
- [SETUP.md](./SETUP.md) - Detailed setup guide
- [COMPONENTS.md](./COMPONENTS.md) - Component reference
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture

## 🔗 Useful Links

- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion)
- [Zustand](https://zustand-demo.vercel.app)
- [Axios](https://axios-http.com)

## 💡 Pro Tips

1. **Hot Reload**: Changes auto-reload in browser
2. **DevTools**: Install React DevTools extension
3. **Network Tab**: Debug API calls here
4. **Console**: Check for JavaScript errors
5. **Component Tree**: Use React DevTools to inspect
6. **Styles Inspector**: Check which Tailwind classes apply

## 📦 Production Deployment

```bash
# Build
npm run build

# Upload dist/ folder to:
# - Vercel
# - Netlify
# - GitHub Pages
# - Traditional hosting

# Set env variables:
# VITE_API_URL=https://api.yourdomain.com
```

## 🎓 Learning Path

1. **Start**: Run `npm run dev` and explore UI
2. **Understand**: Read SETUP.md and ARCHITECTURE.md
3. **Build**: Create new component following patterns
4. **Integrate**: Add API calls using endpoints.js
5. **Deploy**: Follow production deployment steps

## 🤝 Contributing Guidelines

- Follow existing code style
- Use meaningful variable names
- Comment complex logic
- Test before submitting
- Keep components small and focused
- Reuse existing components

## 📞 Support

- Check error messages in console
- Review documentation files
- Look at similar components for examples
- Inspect Network tab for API issues
- Check backend logs for errors

---

**Version**: 1.0.0
**Built with**: React 18 + Vite
**Status**: ✅ Production Ready

🚀 Ready to rock! Start with `npm run dev`
