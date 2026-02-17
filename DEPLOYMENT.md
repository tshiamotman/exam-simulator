# Deployment & Configuration Guide

This document explains how to configure the exam simulator for different environments.

## Configuration Files

### 1. `config.js` (Default Configuration)
This is the main configuration file with sensible defaults. It contains:
- **API Configuration**: Base URL for API calls
- **Environment**: Application environment (development/staging/production)
- **Debug Mode**: Enable/disable verbose logging
- **Exam Settings**: Auto-save intervals and time warnings

### 2. `config.local.js` (Environment-Specific Overrides)
Create this file to override settings for your specific environment. It is **not committed to git** and should be created on each deployment target.

## Setup Instructions

### Development Setup

1. The default configuration is already set for local development:
   ```javascript
   API_BASE: 'http://localhost:8000/api'
   environment: 'development'
   debug: true
   ```

2. Run the backend server:
   ```bash
   cd d:\Projects\exam-simulator
   python app.py
   ```

3. Open `exam.html` in your browser at `http://localhost:8000`

### Important: Configuration File Serving

The FastAPI backend serves configuration files directly from the project root:

- `config.js` is served at `http://localhost:8000/config.js`
- `config.local.js` is served at `http://localhost:8000/config.local.js` (optional, with graceful fallback)

The HTML automatically loads these files from these routes. Both files must be in the project root directory alongside `exam.html`.

### Production Deployment

1. **Create `config.local.js`** on your production server:
   ```javascript
   const CONFIG_LOCAL = {
       api: {
           baseUrl: 'https://yourdomain.com/api'  // Your production API URL
       },
       environment: 'production',
       debug: false,
       exam: {
           autoSaveInterval: 10000,
           timeWarnings: {
               critical: 300,
               warning: 600
           }
       }
   };
   ```

2. **Ensure `exam.html` is served** alongside `config.js` and `config.local.js`

3. **Configure your backend** to run on your production server

### Staging Deployment

Similar to production, but with staging credentials:
```javascript
const CONFIG_LOCAL = {
    api: {
        baseUrl: 'https://staging.yourdomain.com/api'
    },
    environment: 'staging',
    debug: true
};
```

## Configuration Options

### API Configuration

```javascript
api: {
    baseUrl: 'http://localhost:8000/api'  // Full URL to API endpoint
}
```

### Environment

```javascript
environment: 'development'  // 'development', 'staging', or 'production'
```

### Debug Mode

```javascript
debug: true  // Enable/disable verbose console logging
```

### Exam Settings

```javascript
exam: {
    autoSaveInterval: 5000,  // Milliseconds between auto-saves
    timeWarnings: {
        critical: 300,       // Alert at 5 minutes remaining
        warning: 600         // Alert at 10 minutes remaining
    }
}
```

## Loading Priority

The application loads configuration in this order:
1. `config.js` (default values)
2. `config.local.js` (overrides, optional)

If `config.local.js` is not found, the application uses defaults with a console message.

## Template Files

- **`.env.example`**: Reference for environment variables
- **`config.local.example.js`**: Template showing example configurations for different environments

## Important Notes

- **Never commit `config.local.js` to version control** - it contains environment-specific settings
- The `.gitignore` file already includes `config.local.js`, `.env`, and similar files
- Always test configuration changes in development/staging before deploying to production
- The `debug` flag should be `false` in production to avoid exposing sensitive information

## Troubleshooting

### API Calls Failing
1. Check the browser console (F12) for errors
2. Verify `API_BASE` is correctly set in `config.js` or `config.local.js`
3. Ensure your backend API is accessible from the client browser
4. Check for CORS issues if frontend and backend are on different domains

### Configuration Not Changing
1. Verify `config.local.js` exists in the same directory as `exam.html`
2. Check browser cache - do a hard refresh (Ctrl+Shift+R)
3. Check browser console for any configuration loading errors

### Static Files Not Loading (404 errors for config.js, config.local.js)
1. Check that the FastAPI backend is running: `python app.py`
2. Verify in browser console that files are requested from root paths:
   - `http://localhost:8000/config.js`
   - `http://localhost:8000/config.local.js` (optional)
3. Ensure `config.js` and `config.local.js` exist in the project root directory
4. The backend serves these files directly - restart the backend if files are moved or added
5. Check the backend console for 404 errors (which indicate missing files)
6. For production, ensure both files are deployed with the backend code

### Local Development Issues
1. Ensure Python backend is running on `http://localhost:8000`
2. Verify the HTML file loads locally or via a simple server
3. Check that `config.js` is in the same directory as `exam.html`
