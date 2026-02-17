/**
 * Example: Local Configuration File (config.local.js)
 * 
 * Copy sections from this file to create your config.local.js file.
 * DO NOT commit config.local.js to version control.
 * The .gitignore already includes config.local.js.
 * 
 * Each section shows a complete example for different environments.
 */

// ============================================================================
// EXAMPLE 1: DEVELOPMENT ENVIRONMENT
// ============================================================================
// Use this for local development with a local backend server
/*
const CONFIG_LOCAL = {
    api: {
        baseUrl: 'http://localhost:8000/api'
    },
    environment: 'development',
    debug: true,
    exam: {
        autoSaveInterval: 5000,
        timeWarnings: {
            critical: 300,
            warning: 600
        }
    }
};
*/

// ============================================================================
// EXAMPLE 2: STAGING ENVIRONMENT
// ============================================================================
// Use this when deploying to a staging server
/*
const CONFIG_LOCAL = {
    api: {
        baseUrl: 'https://staging.yourdomain.com/api'
    },
    environment: 'staging',
    debug: true,  // Enable debug in staging to see issues
    exam: {
        autoSaveInterval: 5000,
        timeWarnings: {
            critical: 300,
            warning: 600
        }
    }
};
*/

// ============================================================================
// EXAMPLE 3: PRODUCTION ENVIRONMENT
// ============================================================================
// Use this when deploying to production
/*
const CONFIG_LOCAL = {
    api: {
        baseUrl: 'https://api.yourdomain.com/api'
    },
    environment: 'production',
    debug: false,  // Always disable debug in production
    exam: {
        autoSaveInterval: 10000,  // Longer interval in production
        timeWarnings: {
            critical: 300,
            warning: 600
        }
    }
};
*/

// ============================================================================
// IMPLEMENTATION NOTES
// ============================================================================
/*
 * 1. Copy ONE of the sections above to the actual config.local.js file
 * 2. Uncomment the code 
 * 3. Update the values for your specific environment
 * 4. Save the file as config.local.js in the same directory as exam.html
 * 
 * The config.local.js file will:
 * - Automatically merge with config.js defaults
 * - Override only the settings you specify
 * - Load after config.js but before the React app starts
 * - NOT be committed to git (safely ignored by .gitignore)
 */

// NOTE: config.local.js is NOT included in version control.
// Please NEVER commit this file to git.
