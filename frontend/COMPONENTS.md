# Agent Platform Frontend - Components Index

## Core Components

### Button.jsx
Interactive button component with multiple variants and sizes.

**Props:**
- `variant`: 'primary' | 'secondary' | 'danger' | 'ghost' | 'outline'
- `size`: 'sm' | 'md' | 'lg'
- `loading`: boolean
- `disabled`: boolean
- `fullWidth`: boolean
- `icon`: React component
- `children`: React node

**Example:**
```jsx
<Button variant="primary" size="lg" icon={Plus} loading={isLoading}>
  Create New
</Button>
```

### Input.jsx
Controlled input field with validation support.

**Props:**
- `label`: string
- `type`: string (default: 'text')
- `icon`: React component (optional)
- `error`: string (error message)
- `placeholder`: string
- All standard HTML input attributes

**Example:**
```jsx
<Input
  label="Email"
  type="email"
  icon={Mail}
  error={errors.email}
  placeholder="user@example.com"
/>
```

### Card.jsx
Reusable card component with gradient background.

**Props:**
- `children`: React node
- `className`: string (additional classes)
- All motion div props

**Example:**
```jsx
<Card className="max-w-md">
  <h2>Card Title</h2>
  <p>Card content</p>
</Card>
```

### Navbar.jsx
Navigation bar with responsive mobile menu.

**Features:**
- Logo and branding
- Navigation links
- User profile display
- Mobile hamburger menu
- Protected route indicators

### ProtectedRoute.jsx
Wrapper component for protected routes.

**Usage:**
```jsx
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

### PageLoader.jsx
Full-screen loading spinner.

**Usage:**
```jsx
{isLoading ? <PageLoader /> : <Content />}
```

### Toast.jsx
Toast notification component.

**Props:**
- `type`: 'success' | 'error' | 'info'
- `title`: string
- `message`: string
- `onClose`: function

## Page Components

### Home.jsx
Landing page with feature showcase and CTAs.

### Login.jsx
User login form with email/username support.

### Register.jsx
User registration with two-step verification (signup + OTP).

### Dashboard.jsx
User dashboard with stats and quick actions.

### Chat.jsx
Chat interface with thread management and streaming responses.

### Resume.jsx
Resume upload and analysis page.

## Store (Zustand)

### authStore
- `user`: Current user object
- `accessToken`: JWT access token
- `refreshToken`: JWT refresh token
- `setUser()`: Update user
- `setAccessToken()`: Set access token
- `logout()`: Clear auth data

### chatStore
- `threads`: Array of chat threads
- `currentThreadId`: Active thread ID
- `messages`: Array of messages
- `createNewThread()`: Create new chat
- `addMessage()`: Add message to chat

### resumeStore
- `resume`: Resume data
- `analysis`: Resume analysis results
- `skillGaps`: Skill gap data
- `setResume()`: Set resume
- `clearResume()`: Clear all resume data

## Services

### api.js
Configured Axios instance with:
- Base URL configuration
- JWT token injection
- Automatic token refresh
- Error handling

### endpoints.js
API endpoint functions grouped by domain:
- `authAPI`: Authentication endpoints
- `chatbotAPI`: Chatbot endpoints
- `resumeAPI`: Resume analysis endpoints

---

For detailed usage, refer to individual component/page files.
