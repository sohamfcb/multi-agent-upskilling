# Frontend Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Application                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Pages/Routes                             │   │
│  │  ├── Home (Landing Page)                             │   │
│  │  ├── Login/Register (Auth)                           │   │
│  │  ├── Dashboard (Protected)                           │   │
│  │  ├── Chat (Protected)                                │   │
│  │  └── Resume (Protected)                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            Reusable Components                        │   │
│  │  ├── Button, Input, Card                             │   │
│  │  ├── Navbar, ProtectedRoute                          │   │
│  │  └── PageLoader, Toast                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          State Management (Zustand)                  │   │
│  │  ├── authStore (User, Tokens)                        │   │
│  │  ├── chatStore (Threads, Messages)                   │   │
│  │  └── resumeStore (Resume Data)                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          API Layer (Services)                         │   │
│  │  ├── api.js (Axios + Interceptors)                   │   │
│  │  └── endpoints.js (API Functions)                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
└─────────────────────────────────────────────────────────────┘
           HTTP (JSON/Streaming)
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                  Backend API (FastAPI)                       │
│  /auth, /core, /api endpoints                                │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Authentication Flow
```
User Input (Login/Register)
         ↓
  Form Component
         ↓
  API Call (endpoints.js)
         ↓
  Backend Response
         ↓
  Update authStore (tokens, user)
         ↓
  localStorage (persist)
         ↓
  Redirect to Dashboard
```

### Chat Flow
```
User Message
     ↓
Chat Component (input)
     ↓
chatStore.addMessage() (user message)
     ↓
chatbotAPI.sendMessage()
     ↓
API Interceptor (add auth token)
     ↓
Backend /core/get-response
     ↓
Streaming Response (NDJSON)
     ↓
Parse chunks & update chatStore
     ↓
Display in Chat Component
```

### Resume Upload Flow
```
File Selection
     ↓
Handle Drop/Change
     ↓
Validate (type, size)
     ↓
resumeAPI.uploadResume(file)
     ↓
FormData with file
     ↓
Backend processes
     ↓
resumeAPI.analyzResume()
     ↓
resumeAPI.getSkillGaps()
     ↓
Update resumeStore
     ↓
Display Analysis Results
```

## Component Hierarchy

```
App
├── Navbar
│   ├── Logo
│   ├── NavLinks
│   ├── UserMenu
│   └── MobileMenu
├── Routes
│   ├── Home
│   │   ├── Hero
│   │   ├── FeatureCards
│   │   └── CTA
│   ├── Login
│   │   └── LoginForm
│   ├── Register
│   │   ├── RegisterForm
│   │   └── OTPVerification
│   ├── Dashboard (Protected)
│   │   ├── StatsGrid
│   │   ├── QuickLinks
│   │   ├── RecentActivities
│   │   └── CTA
│   ├── Chat (Protected)
│   │   ├── Sidebar (Threads)
│   │   ├── MessageArea
│   │   └── InputForm
│   └── Resume (Protected)
│       ├── UploadArea
│       └── AnalysisDisplay
└── Toaster (Notifications)
```

## State Management Structure

```
Zustand Stores
│
├── authStore
│   ├── user (object)
│   ├── accessToken (string)
│   ├── refreshToken (string)
│   ├── isLoading (boolean)
│   ├── error (string)
│   └── methods
│       ├── setUser()
│       ├── setAccessToken()
│       ├── logout()
│       └── isAuthenticated()
│
├── chatStore
│   ├── threads (array)
│   ├── currentThreadId (string)
│   ├── messages (array)
│   ├── isLoading (boolean)
│   └── methods
│       ├── setThreads()
│       ├── addMessage()
│       └── createNewThread()
│
└── resumeStore
    ├── resume (object)
    ├── analysis (object)
    ├── skillGaps (object)
    ├── isLoading (boolean)
    └── methods
        ├── setResume()
        ├── setAnalysis()
        └── clearResume()
```

## API Integration Pattern

```
Service Layer (endpoints.js)
│
├── authAPI
│   ├── register(data)
│   ├── login(data)
│   ├── logout()
│   └── refresh(token)
│
├── chatbotAPI
│   ├── sendMessage(msg, threadId)
│   ├── getChatHistory(threadId)
│   └── getAllThreads()
│
└── resumeAPI
    ├── uploadResume(file)
    ├── analyzResume(text)
    └── getSkillGaps(text, jobDesc)
        ↓
    axiosInstance
    │
    ├── Request Interceptor
    │   └── Add JWT token
    │
    ├── Response Interceptor
    │   ├── Check status
    │   ├── Handle 401 (token refresh)
    │   └── Return response
    │
    └── Axios Config
        ├── Base URL
        ├── Headers
        └── Timeout
```

## Routing Architecture

```
/
├── / (Home - Public)
├── /login (Login - Public)
├── /register (Register - Public)
└── Protected Routes (Require Auth)
    ├── /dashboard (Dashboard)
    ├── /chat (Chat)
    └── /resume (Resume)
    
ProtectedRoute Component
├── Check: useAuthStore.isAuthenticated()
├── Yes: Render component
└── No: Redirect to /login
```

## Styling Architecture

```
Tailwind CSS
├── Configuration (tailwind.config.js)
│   ├── Colors (custom palette)
│   ├── Fonts
│   ├── Animations
│   └── Breakpoints
│
└── Global Styles (styles/globals.css)
    ├── Base styles
    ├── Component utilities
    └── Scroll styling
    
Component Styling
├── Inline Tailwind classes
├── Framer Motion animations
├── CSS variables (gradients)
└── Responsive design (sm:, md:, lg:, etc.)
```

## Performance Optimization

```
Code Splitting
├── Route-based splitting
├── Lazy component loading
└── Dynamic imports

Bundle Optimization
├── Tree shaking
├── CSS purging
├── Minification
└── Compression

Caching
├── Browser cache
├── localStorage (auth tokens)
└── API response caching

Rendering Optimization
├── useCallback (memoize functions)
├── useMemo (memoize values)
├── React.memo (memoize components)
└── Lazy loading images
```

## Error Handling Strategy

```
API Errors
├── 4xx (Client errors)
│   ├── 400: Bad request → Show form errors
│   ├── 401: Unauthorized → Refresh token
│   └── 404: Not found → Redirect
│
└── 5xx (Server errors)
    └── Show generic error message

Form Validation
├── Client-side validation
├── Server-side validation errors
└── Show inline error messages

Network Errors
├── Connection timeout
├── No internet
└── Show offline indicator

User Feedback
├── Toast notifications (success/error)
├── Loading spinners
├── Error messages
└── Success confirmations
```

## Security Measures

```
Authentication
├── JWT tokens (access + refresh)
├── Token stored in Zustand + localStorage
├── Automatic token refresh
└── Secure logout

Authorization
├── Protected routes (ProtectedRoute)
├── Role-based access (future)
└── Token validation on each request

Data Protection
├── HTTPS in production
├── XSS prevention (React escaping)
├── CSRF tokens (if needed)
└── Input validation

API Security
├── Request interceptors (add auth)
├── Response interceptors (handle errors)
├── Secure CORS configuration
└── Rate limiting (backend)
```

## Development Workflow

```
Local Development
├── npm run dev (Vite dev server)
├── Hot Module Replacement (HMR)
├── Source maps
└── Console debugging

Building
├── npm run build (Vite build)
├── Optimization
├── Output: dist/ directory
└── Ready for deployment

Quality Assurance
├── npm run lint (ESLint)
├── npm run format (Prettier)
└── Manual testing

Deployment
├── Build artifacts
├── Environment variables
├── CDN distribution
└── Performance monitoring
```

---

**Architecture Version**: 1.0
**Last Updated**: 2024
**Status**: Production Ready
