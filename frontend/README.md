# Frontdesk AI - Supervisor Dashboard

React-based supervisor dashboard for the Frontdesk AI Receptionist system.

## Features

- **Dashboard**: Real-time statistics and system overview
- **Pending Requests**: View and respond to escalated questions
- **Request History**: Complete audit trail of all interactions
- **Knowledge Base**: View and manage learned answers
- **Call Simulator**: Test the AI with various scenarios
- **Real-time Updates**: WebSocket notifications for new requests

## Tech Stack

- **React 18**: UI framework
- **TailwindCSS**: Styling
- **React Router**: Navigation
- **Axios**: HTTP client
- **WebSocket**: Real-time communication

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Configuration

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## Available Scripts

- `npm start` - Start development server (port 3000)
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Project Structure

```
src/
├── components/
│   ├── Dashboard.js          # Main dashboard with stats
│   ├── PendingRequests.js    # Handle escalated requests
│   ├── RequestHistory.js     # View all requests
│   ├── KnowledgeBase.js      # Manage knowledge entries
│   └── CallSimulator.js      # Test AI responses
├── App.js                    # Main app with routing
├── index.js                  # Entry point
├── config.js                 # API configuration
└── index.css                 # Global styles
```

## Components

### Dashboard
- System statistics
- Quick action buttons
- System status indicators

### Pending Requests
- List of escalated questions
- Respond to requests inline
- Real-time updates via WebSocket

### Request History
- Filter by status (all, resolved, unresolved)
- View supervisor responses
- Timestamps and customer info

### Knowledge Base
- Search learned answers
- Add new knowledge manually
- View usage statistics

### Call Simulator
- Test AI with custom questions
- Quick fill with sample data
- View escalation results

## Real-time Features

The app connects to the backend via WebSocket for instant notifications:

- New help requests
- Request resolutions
- System events

Connection status shown in header.

## Styling

Uses TailwindCSS utility classes for styling:

- Responsive design
- Modern UI components
- Consistent color scheme
- Accessible components

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development

```bash
# Start with hot reload
npm start

# Lint code
npm run lint

# Format code
npm run format
```

## Deployment

```bash
# Build production bundle
npm run build

# Serve build folder
# Deploy to Netlify, Vercel, or any static host
```

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_WS_URL`: WebSocket URL
- `REACT_APP_ENV`: Environment (development/production)

## Troubleshooting

### Can't connect to backend
- Verify backend is running on port 8000
- Check CORS settings in backend
- Verify API URL in config.js

### WebSocket disconnects
- Check backend WebSocket endpoint
- Verify network connectivity
- Check browser console for errors

### Build fails
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear cache: `npm cache clean --force`
- Update dependencies: `npm update`

## License

MIT
