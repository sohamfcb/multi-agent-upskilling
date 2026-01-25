# Frontend Deployment Guide

## 🚀 Deployment Options

### Option 1: Vercel (Recommended - Easiest)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/repo.git
   git push -u origin main
   ```

2. **Deploy on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Select your repository
   - Framework: React
   - Build command: `npm run build`
   - Output directory: `dist`
   - Environment variables:
     ```
     VITE_API_URL=https://api.yourdomain.com
     ```
   - Click Deploy

3. **Done!** Your site is live

### Option 2: Netlify

1. **Push to GitHub** (same as Vercel)

2. **Deploy on Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Select your repository
   - Build settings:
     - Build command: `npm run build`
     - Publish directory: `dist`
   - Advanced settings:
     - Environment variables:
       ```
       VITE_API_URL=https://api.yourdomain.com
       ```
   - Deploy site

3. **Configure redirects** (create `public/_redirects`):
   ```
   /* /index.html 200
   ```

### Option 3: Traditional Hosting (Shared/VPS)

1. **Build locally**
   ```bash
   npm run build
   ```

2. **Upload `dist/` folder**
   - Use FTP/SFTP client
   - Upload entire `dist` folder contents to `public_html/`

3. **Server Configuration**
   - Configure web server (Apache/Nginx) for SPA:
   
   **Nginx:**
   ```nginx
   location / {
     try_files $uri $uri/ /index.html;
   }
   ```
   
   **Apache:** (in `.htaccess`)
   ```
   <IfModule mod_rewrite.c>
     RewriteEngine On
     RewriteBase /
     RewriteRule ^index\.html$ - [L]
     RewriteCond %{REQUEST_FILENAME} !-f
     RewriteCond %{REQUEST_FILENAME} !-d
     RewriteRule . /index.html [L]
   </IfModule>
   ```

4. **SSL Certificate**
   - Use Let's Encrypt (free)
   - Or purchase from provider

### Option 4: Docker + Kubernetes

1. **Create Dockerfile**
   ```dockerfile
   # Build stage
   FROM node:18-alpine as build
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build

   # Production stage
   FROM node:18-alpine
   WORKDIR /app
   RUN npm install -g serve
   COPY --from=build /app/dist ./dist
   EXPOSE 3000
   CMD ["serve", "-s", "dist", "-l", "3000"]
   ```

2. **Build Docker image**
   ```bash
   docker build -t agent-frontend:latest .
   docker run -p 3000:3000 agent-frontend:latest
   ```

3. **Push to registry**
   ```bash
   docker tag agent-frontend yourusername/agent-frontend
   docker push yourusername/agent-frontend
   ```

4. **Deploy to Kubernetes**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: frontend
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: frontend
     template:
       metadata:
         labels:
           app: frontend
       spec:
         containers:
         - name: frontend
           image: yourusername/agent-frontend:latest
           ports:
           - containerPort: 3000
           env:
           - name: VITE_API_URL
             value: "https://api.yourdomain.com"
   ```

## 🔧 Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] API endpoints point to production backend
- [ ] Build runs without errors: `npm run build`
- [ ] No console errors or warnings
- [ ] All features tested in production build
- [ ] Images optimized
- [ ] Meta tags updated (favicon, title, description)
- [ ] Analytics setup (if needed)

## 📝 Environment Variables

### Development
```env
VITE_API_URL=http://localhost:8000
```

### Production
```env
VITE_API_URL=https://api.yourdomain.com
```

## 🔒 Security Checklist

- [ ] HTTPS enabled
- [ ] API uses HTTPS
- [ ] CORS properly configured
- [ ] Security headers set (backend)
- [ ] No sensitive data in code/env
- [ ] Dependencies updated
- [ ] No debug mode in production

## 📊 Performance Optimization

### Before Deployment

```bash
# Check bundle size
npm run build

# Analyze bundle
npm install -D vite-plugin-visualizer
# Add to vite.config.js and build
```

### After Deployment

- Enable gzip compression on server
- Set cache headers:
  ```
  Cache-Control: max-age=31536000 (for assets)
  Cache-Control: no-cache (for index.html)
  ```
- Enable HTTP/2
- Use CDN for assets

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm ci
      - run: npm run build
      
      - uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

## 🚨 Common Deployment Issues

### Issue: Blank page on load
**Solution**: Check that `dist/index.html` is being served for all routes

### Issue: API 404 errors
**Solution**: Verify `VITE_API_URL` matches backend URL

### Issue: Styles not loading
**Solution**: Check CSS files in `dist/` folder, verify CSS paths

### Issue: Broken images
**Solution**: Use relative paths for images, ensure they're in `dist/`

### Issue: localStorage errors
**Solution**: Check browser storage quota, clear old data

### Issue: Token refresh failing
**Solution**: Verify backend refresh endpoint, check CORS headers

## 📈 Monitoring

### Setup Error Tracking
```javascript
// Add to App.jsx for production
import * as Sentry from "@sentry/react";

if (process.env.NODE_ENV === 'production') {
  Sentry.init({
    dsn: "YOUR_SENTRY_DSN",
    environment: "production",
    tracesSampleRate: 0.1,
  });
}
```

### Monitor Performance
- Use Lighthouse in DevTools
- Monitor Core Web Vitals
- Track API response times
- Monitor error rates

## 🔄 Updates & Maintenance

### Deploy Updates
```bash
# Make changes
git add .
git commit -m "Fix: description"
git push origin main

# Automatic deployment (if CI/CD configured)
# Or manual deployment through platform dashboard
```

### Cache Busting
- Vite automatically adds hash to filenames
- No cache headers for `index.html`
- Long cache headers for assets

## 🆘 Rollback Plan

### Vercel
- Go to Deployments tab
- Click on previous deployment
- Click "Promote to Production"

### Netlify
- Go to Deployments
- Publish previous deployment

### Manual
- Keep backup of previous `dist` folder
- Restore from backup if needed

## 📞 Support & Debugging

### Check Deployment Logs
- Vercel: Deployments → Logs
- Netlify: Deploys → Details → Logs
- Traditional: Server logs (check with host)

### Common Log Errors
```
"Cannot find module" → Missing dependency
"Build failed" → Syntax error in code
"Port already in use" → Change port in config
```

## 📚 Deployment Resources

- [Vercel Docs](https://vercel.com/docs)
- [Netlify Docs](https://docs.netlify.com)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)
- [Docker Docs](https://docs.docker.com)

## 🎯 Recommended Deployment

**For Most Users**: Vercel
- ✅ Free tier available
- ✅ Automatic deployments
- ✅ Global CDN
- ✅ Built-in analytics
- ✅ Simple configuration

**For Enterprises**: Custom VPS + CI/CD
- Full control
- Custom domain
- Custom infrastructure
- Dedicated support

---

**Happy Deploying! 🚀**
