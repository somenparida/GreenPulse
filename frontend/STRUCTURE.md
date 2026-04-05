# Frontend Folder Structure

```
frontend/
├── public/                 # Static files
│   └── [assets here]
├── src/                    # Source code
│   ├── App.tsx             # Main application component
│   ├── main.tsx            # React entry point
│   ├── index.css           # Global styles
│   ├── api.ts              # API utilities (NEW)
│   ├── hooks.ts            # Custom React hooks (NEW)
│   └── [components/]       # (Future component hierarchy)
├── .eslintrc.cjs           # ESLint configuration
├── .eslintrc.md            # ESLint documentation
├── .prettierrc.json        # Prettier configuration
├── .prettierignore         # Prettier ignore patterns
├── .gitignore              # Git ignore patterns
├── .env.example            # Environment variables template
├── .dockerignore           # Docker ignore patterns
├── Dockerfile              # Docker image definition
├── index.html              # HTML entry point
├── package.json            # Dependencies & scripts
├── package-lock.json       # Locked versions
├── tsconfig.json           # TypeScript configuration
├── tsconfig.node.json      # TypeScript Node configuration
├── vite.config.ts          # Vite build configuration
├── vite-env.d.ts           # TypeScript environment types
├── README.md               # Frontend documentation
├── TROUBLESHOOTING.md      # Troubleshooting guide (NEW)
└── STRUCTURE.md            # This file
```

## Key Files Explained

### `src/App.tsx`
Main React component that displays the sensor dashboard.
- Fetches readings from backend API
- Handles loading and error states
- Displays readings in a grid layout
- Includes retry mechanism

### `src/main.tsx`
React application entry point.
- Initializes React 18 root
- Renders App component
- Error handling for missing root element

### `src/index.css`
Global styles for the application.
- CSS custom properties (variables)
- Dark theme styling
- Responsive grid layout
- Component-specific styles

### `src/api.ts` (NEW)
API utility functions.
- Axios client configuration
- Request/response interceptors
- Centralized API management

### `src/hooks.ts` (NEW)
Custom React hooks.
- `useFetch` hook for data fetching
- Reusable data loading logic
- Error handling

### `Dockerfile`
Multi-stage Docker build for production.
- Build stage with dependencies
- Runtime stage with serve
- Optimized for production

### `vite.config.ts`
Vite build tool configuration.
- Development server setup
- API proxy configuration
- Build optimization
- Code splitting rules

### `package.json`
Dependencies and scripts.
- React, React-DOM, Axios
- Dev tools: Vite, ESLint, Prettier, TypeScript
- Scripts: dev, build, lint, format

## Development Workflow

### Adding New Features

1. **Create component** (when needed):
   ```bash
   mkdir -p src/components/FeatureName
   touch src/components/FeatureName/index.tsx
   ```

2. **Use hooks** for data fetching:
   ```tsx
   import { useFetch } from '../hooks'
   const { data, error, loading } = useFetch('/api/v1/readings')
   ```

3. **Format and lint**:
   ```bash
   npm run format
   npm run lint -- --fix
   ```

4. **Test build**:
   ```bash
   npm run build
   ```

### Adding Dependencies

```bash
# Add to package.json
npm install package-name

# Add dev dependency
npm install --save-dev package-name

# Update when building Docker image
docker-compose build frontend
```

## Type Safety

TypeScript configuration enforces:
- Strict null checks
- No implicit any
- Strict function types
- Unused variable detection

### Type Definitions

- `SensorReading` - API response interface
- `ApiError` - Error response interface
- Custom hook return types

## Performance Considerations

### Bundle Size
- Vendor code: React, React-DOM, Axios
- App code: App component, hooks, styles
- Optimized imports prevent bundle bloat

### Runtime Performance
- Auto-refresh every 5 seconds (configurable)
- Efficient re-renders with React.StrictMode
- Event delegation for event handlers

## Testing

### Pre-commit Checks
```bash
# Run all checks
npm run lint
npm run format
npm run build
```

### Manual Testing
```bash
# Development mode
npm run dev

# Test build
npm run build
npm run preview
```

## Deployment

### Docker
```bash
docker build -t greenpulse-frontend .
docker run -p 3000:3000 -e VITE_API_URL=http://api.example.com greenpulse-frontend
```

### Static Hosting
```bash
npm run build
# Contents of dist/ folder can be deployed to any static host
```

### Environment Variables
Set `VITE_API_URL` before build or runtime:
```bash
VITE_API_URL=https://api.production.com npm run build
```
