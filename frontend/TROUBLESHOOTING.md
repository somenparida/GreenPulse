# Frontend Troubleshooting Guide

## Common Issues

### 1. API Connection Issues

**Problem**: "Failed to fetch sensor readings"

**Solutions**:
```bash
# Make sure backend is running
docker-compose -f docker-compose.full.yml up -d backend

# Check backend is accessible
curl http://localhost:8000/health

# Verify VITE_API_URL environment variable
echo $VITE_API_URL  # Should show http://localhost:8000

# If using Docker, API URL should be http://backend:8000
VITE_API_URL=http://backend:8000 npm run dev
```

### 2. Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use different port
npm run dev -- --port 3001
```

### 3. Build Fails

```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json dist
npm install
npm run build
```

### 4. TypeScript Errors

```bash
# Check TypeScript compilation
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix

# Format code
npm run format
```

### 5. Hot Module Replacement (HMR) Not Working

```bash
# Restart dev server
npm run dev

# If still not working, clear vite cache
rm -rf .vite
npm run dev
```

## Development Tips

### Debug API Calls

Add to `src/App.tsx`:
```tsx
useEffect(() => {
  console.log('Current API URL:', import.meta.env.VITE_API_URL)
}, [])
```

### Check Network Requests

1. Open DevTools (F12)
2. Go to Network tab
3. Look for `/api/v1/readings` requests
4. Check response status and data

### Slow Performance

```bash
# Check bundle size
npm run build
du -sh dist/

# Analyze more details
npm install --save-dev webpack-bundle-analyzer
```

## Environment Configuration

### .env.local

```env
# Local development
VITE_API_URL=http://localhost:8000

# With Docker
VITE_API_URL=http://backend:8000

# Production
VITE_API_URL=https://api.greenpulse.com
```

### From Docker

Set environment when running container:
```bash
docker run -e VITE_API_URL=http://backend:8000 greenpulse-frontend
```

## Performance Optimization

### Code Splitting

Already configured in `vite.config.ts`:
```ts
rollupOptions: {
  output: {
    manualChunks: {
      vendor: ['react', 'react-dom', 'axios'],
    },
  },
}
```

### Lazy Loading

```tsx
import { lazy, Suspense } from 'react'

const DashboardComponent = lazy(() => import('./Dashboard'))

<Suspense fallback={<div>Loading...</div>}>
  <DashboardComponent />
</Suspense>
```

## Testing

### Run Linter
```bash
npm run lint
```

### Format Code
```bash
npm run format
```

### Type Check
```bash
npm run build  # This checks types
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Getting Help

1. Check Browser DevTools Console for errors
2. Look at Network tab for failed requests
3. Check backend logs
4. Review GitHub issues
