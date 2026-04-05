# GreenPulse Frontend

Modern React dashboard for agricultural IoT sensor data visualization.

## Features

- ✨ Real-time sensor data display
- 📊 Responsive grid layout
- 🎨 Dark theme UI
- ⚡ Fast development with Vite
- 🔒 TypeScript for type safety
- 🧪 Linting with ESLint
- 💅 Code formatting with Prettier

## Quick Start

### Development
```bash
# Install dependencies
npm install

# Start dev server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Preview build
npm run preview
```

### Linting & Formatting
```bash
# Check code quality
npm run lint

# Format code
npm run format
```

## Project Structure

```
src/
├── App.tsx          # Main application component
├── index.css        # Global styles
└── main.tsx         # React entry point
```

## API Integration

The frontend fetches sensor data from the backend API:

- **API Base URL**: Configurable via `VITE_API_URL` environment variable
- **Default**: `http://localhost:8000`

### Environment Variables

Create `.env.local`:
```env
VITE_API_URL=http://localhost:8000
```

## Docker

Build and run in Docker:

```bash
# Build image
docker build -t greenpulse-frontend .

# Run container
docker run -p 3000:3000 greenpulse-frontend
```

## Technologies

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Axios** - HTTP client
- **ESLint** - Code quality
- **Prettier** - Code formatting

## Development Guidelines

### Code Style

Follow the ESLint and Prettier configuration automatically:

```bash
# Automatically fix issues
npm run lint -- --fix
npm run format
```

### Component Guidelines

- Use functional components with hooks
- Type all props and state
- Keep components small and focused
- Use meaningful variable names

## Performance

- Auto-refresh every 5 seconds
- Proper error handling and retry logic
- Optimized for production builds
- Lazy loading ready

## Troubleshooting

### "Failed to fetch sensor readings"
- Check backend is running at `VITE_API_URL`
- Verify CORS is enabled in backend
- Check network tab in DevTools

### Build fails
```bash
# Clear cache and rebuild
rm -rf dist node_modules
npm install
npm run build
```

### Port already in use
```bash
# Use different port
npm run dev -- --port 3001
```

## Support

For issues and questions, refer to the main [README.md](../README.md).

## License

MIT License - See [LICENSE](../LICENSE)
