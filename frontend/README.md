# Frontend - Agent Platform

Modern, responsive React frontend for the multi-agent upskilling platform.

## 🚀 Features

- **Authentication**: Secure login/registration with OTP verification
- **Dashboard**: Overview of progress and analytics
- **Chatbot**: Real-time conversations with AI agents
- **Resume Analyzer**: Upload and analyze resumes with skill gap identification
- **Responsive Design**: Beautiful UI that works on all devices
- **State Management**: Zustand for efficient state handling
- **Modern Tech Stack**: React 18, Vite, Tailwind CSS, Framer Motion

## 📦 Installation

```bash
cd frontend
npm install
```

## 🔧 Configuration

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## 🏃 Running the App

### Development
```bash
npm run dev
```

App will be available at `http://localhost:3000`

### Production Build
```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Button.jsx
│   ├── Input.jsx
│   ├── Card.jsx
│   ├── Navbar.jsx
│   ├── ProtectedRoute.jsx
│   ├── PageLoader.jsx
│   └── Toast.jsx
├── pages/              # Page components
│   ├── Home.jsx
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│   ├── Chat.jsx
│   └── Resume.jsx
├── services/           # API integration
│   ├── api.js          # Axios instance with interceptors
│   └── endpoints.js    # API endpoint functions
├── store/              # State management
│   └── stores.js       # Zustand stores
├── styles/             # Global styles
│   └── globals.css
├── App.jsx             # Main app component
└── main.jsx            # Entry point
```

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (#0ea5e9 - #0284c7)
- **Dark**: Slate palette for modern look
- **Accent**: Purple and cyan for highlights

### Typography
- **Font**: Segoe UI, Roboto, sans-serif
- **Headings**: Bold, gradient text
- **Body**: Regular weight with slate colors

### Components
- Custom styled buttons with hover effects
- Input fields with icons and validation
- Cards with gradient backgrounds
- Smooth animations with Framer Motion
- Toast notifications for feedback

## 🔌 API Integration

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/verify-signup` - Verify OTP
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token
- `PUT /auth/update-username` - Update username
- `PUT /auth/update-password` - Update password

### Chatbot
- `POST /core/get-response` - Send message to chatbot
- `GET /core/chat-history` - Get chat history
- `GET /core/all_threads` - Get all chat threads

### Resume
- `POST /core/upload-resume` - Upload resume file
- `POST /core/analyze-resume` - Analyze resume content
- `POST /core/skill-gaps` - Get skill gap analysis

## 🔐 Security

- JWT tokens stored in Zustand store
- Automatic token refresh with interceptors
- Protected routes require authentication
- XSS protection with React's built-in escaping
- CORS configured on backend

## 🎯 Best Practices

- Component composition and reusability
- Proper error handling and user feedback
- Loading states during API calls
- Responsive design with Tailwind CSS
- Smooth animations and transitions
- Clean code organization

## 📝 Notes

- Ensure backend is running on `http://localhost:8000`
- API endpoint prefix is configured in vite.config.js
- All protected routes redirect to login if not authenticated
- State persists across page refreshes using localStorage

## 🚀 Deployment

### Build
```bash
npm run build
```

### Deploy to Vercel/Netlify
1. Connect your GitHub repository
2. Build command: `npm run build`
3. Output directory: `dist`
4. Set environment variables

### Docker
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 📚 Technologies

- **React 18** - UI library
- **Vite** - Build tool
- **React Router v6** - Routing
- **Zustand** - State management
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Axios** - HTTP client
- **Lucide React** - Icons

---

Built with ❤️ for modern web development
