# IVIE Wedding Studio - Frontend

React frontend for IVIE Wedding Studio website built with Vite.

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env` file:
```
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at: `http://localhost:5173`

### 4. Build for Production

```bash
npm run build
```

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **CSS Modules** - Styling

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/            # API client and endpoints
│   │   └── client.js
│   ├── components/     # Reusable components
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   └── Button.jsx
│   ├── pages/          # Page components
│   │   ├── Home.jsx
│   │   ├── Products.jsx
│   │   └── MakeupServices.jsx
│   ├── styles/         # CSS files
│   │   ├── global.css
│   │   ├── products.css
│   │   └── makeup.css
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Base styles
├── .env                # Environment variables
├── package.json
└── vite.config.js
```

## Pages

### Home
- Hero section
- Services overview
- Call-to-action

### Products
- Product catalog with filtering
- Categories: Modern wedding, Traditional ao dai
- Rental and purchase pricing
- Filter by category and gender

### Makeup Services
- Service packages
- Expert team profiles
- Service features and pricing

## API Integration

All API calls are handled through `src/api/client.js`:

```javascript
import { productsAPI, servicesAPI, contactAPI } from './api/client';

// Get all products
const products = await productsAPI.getAll();

// Get products with filters
const filtered = await productsAPI.getAll({ category: 'wedding_modern' });

// Get experts
const experts = await servicesAPI.getExperts();
```

## Development

- Hot module replacement enabled
- TypeScript support (optional)
- ESLint configured
- Responsive design

## Deployment

Build the production bundle:
```bash
npm run build
```

Deploy the `dist/` folder to:
- Vercel
- Netlify
- GitHub Pages
- Any static hosting service
