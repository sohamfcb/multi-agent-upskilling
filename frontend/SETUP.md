# Frontend Setup & Getting Started

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm installed
- Backend running on `http://localhost:8000`

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Visit `http://localhost:3000` in your browser.

## 📋 Project Structure Overview

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   ├── pages/              # Page components for routes
│   ├── services/           # API integration layer
│   ├── store/              # Zustand state management
│   ├── styles/             # Global CSS
│   ├── App.jsx             # Main application
│   └── main.jsx            # Entry point
├── index.html              # HTML template
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind CSS config
├── postcss.config.js       # PostCSS config
├── package.json            # Dependencies
└── README.md               # Documentation
```

## 🎨 Design System

### Color Palette
- **Primary Blue**: `#0ea5e9` → `#0284c7`
- **Dark Slate**: `#0f172a` (background)
- **Secondary Purple**: `#a855f7`
- **Accent Cyan**: `#06b6d4`

### Typography
- **Headings**: Bold with gradient text effect
- **Body**: Regular Segoe UI/Roboto
- **Small**: Slate-400 for descriptions

### Spacing
- Base unit: 4px
- Use Tailwind's spacing scale (p-4, m-6, etc.)

### Animations
- Smooth fade and slide transitions
- Hover effects on interactive elements
- Loading states with spinning animations
- Page transitions with Framer Motion

## 🔧 Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## 🏃 Development Commands

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Format code
npm run format
```

## 📱 Responsive Design

- **Mobile First**: Design for mobile, enhance for larger screens
- **Breakpoints**:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px

## 🔐 Authentication Flow

1. **Registration**
   - User enters details
   - OTP sent to email
   - User verifies OTP
   - Account created

2. **Login**
   - User enters email/username + password
   - Receives access & refresh tokens
   - Tokens stored in Zustand store & localStorage
   - Redirected to dashboard

3. **Token Refresh**
   - Access token expires after time
   - API interceptor detects 401 response
   - Refresh token used to get new access token
   - Request retried automatically

4. **Logout**
   - Clear auth tokens from store
   - Redirect to login

## 🔌 API Integration

### Request Flow
```
Component → Service (endpoints.js) → API Client (api.js) → Backend
```

### Error Handling
```javascript
try {
  const response = await authAPI.login(data);
  // Handle success
} catch (error) {
  const message = error.response?.data?.message || 'Error';
  // Show error to user
}
```

### Streaming Responses
For chatbot responses, the API returns newline-delimited JSON:
```javascript
const reader = response.data.stream.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const chunk = new TextDecoder().decode(value);
  // Process chunk
}
```

## 🧩 Component Usage Examples

### Creating a Form

```jsx
import { useState } from 'react';
import Button from '../components/Button';
import Input from '../components/Input';
import Card from '../components/Card';

export default function MyForm() {
  const [data, setData] = useState({ email: '' });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // API call
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Email"
          value={data.email}
          onChange={(e) => setData({ email: e.target.value })}
          error={errors.email}
        />
        <Button type="submit" fullWidth loading={loading}>
          Submit
        </Button>
      </form>
    </Card>
  );
}
```

### Using Store

```jsx
import { useAuthStore } from '../store/stores';

export default function MyComponent() {
  const user = useAuthStore((state) => state.user);
  const setUser = useAuthStore((state) => state.setUser);
  const isAuth = useAuthStore((state) => state.isAuthenticated());

  return <div>Welcome {user?.username}</div>;
}
```

### Protected Routes

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

## 🐛 Debugging

### Check Auth Status
```javascript
// In console
localStorage.getItem('auth-store') // View stored auth data
```

### API Calls
- Check Network tab in DevTools
- Verify API_BASE_URL matches backend
- Check CORS configuration in backend

### Component Issues
- Use React DevTools extension
- Check console for errors
- Verify props are passed correctly

## 🚀 Performance Optimization

- Code splitting with React.lazy()
- Image optimization
- CSS purging with Tailwind
- Minification in production build
- Caching with proper headers

## 📦 Dependencies

### Core
- **react** - UI library
- **react-dom** - DOM rendering
- **react-router-dom** - Routing

### State Management
- **zustand** - Lightweight state management

### Styling
- **tailwindcss** - Utility CSS
- **framer-motion** - Animations

### HTTP
- **axios** - HTTP client

### Icons
- **lucide-react** - Icon library

### Notifications
- **react-hot-toast** - Toast notifications

### Build
- **vite** - Build tool
- **@vitejs/plugin-react** - React plugin

## 🔄 Updating Dependencies

```bash
# Check for updates
npm outdated

# Update all
npm update

# Update specific package
npm install package@latest
```

## 📝 Coding Standards

### Component Structure
```jsx
import { hooks, components };

const Component = ({ prop1, prop2 }) => {
  // State
  const [state, setState] = useState();
  
  // Effects
  useEffect(() => {}, []);
  
  // Handlers
  const handleClick = () => {};
  
  // Render
  return <div>{/* JSX */}</div>;
};

export default Component;
```

### Naming Conventions
- Components: PascalCase (Dashboard.jsx)
- Functions: camelCase (handleSubmit)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL)
- Files: kebab-case or PascalCase (Button.jsx)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and test
3. Commit with clear message: `git commit -m "Add feature"`
4. Push and create PR

## 📚 Additional Resources

- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion)
- [Zustand](https://zustand-demo.vercel.app)

## 🆘 Troubleshooting

### Port 3000 already in use
```bash
# Change port in vite.config.js
server: { port: 3001 }
```

### API connection errors
- Check backend is running: `http://localhost:8000`
- Verify CORS is enabled on backend
- Check .env file VITE_API_URL

### Build errors
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

**Questions?** Check the [README.md](./README.md) or [COMPONENTS.md](./COMPONENTS.md)
