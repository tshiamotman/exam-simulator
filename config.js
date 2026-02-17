/**
 * Application Configuration
 * 
 * This file contains all configuration settings for the exam simulator.
 * For environment-specific settings, create a config.local.js file with overrides.
 */

const CONFIG = {
    // API Configuration
    api: {
        // Base URL for API calls
        // Update this to match your backend server
        baseUrl: 'http://localhost:8000/api',
    },
    
    // Application Environment
    // Options: 'development', 'staging', 'production'
    environment: 'development',
    
    // Debug Mode
    // Enable for verbose logging and error details
    debug: true,
    
    // Exam Configuration
    exam: {
        // Auto-save interval in milliseconds
        autoSaveInterval: 5000,
        
        // Show warnings at these time thresholds (in seconds)
        timeWarnings: {
            critical: 300,  // 5 minutes
            warning: 600    // 10 minutes
        }
    }
};

/**
 * Load local overrides if they exist
 * Create a config.local.js file with your environment-specific settings
 * to override the defaults above
 */
if (typeof CONFIG_LOCAL !== 'undefined') {
    // Deep merge CONFIG_LOCAL into CONFIG
    const merge = (target, source) => {
        for (const key in source) {
            if (source[key] instanceof Object && !Array.isArray(source[key])) {
                target[key] = merge(target[key] || {}, source[key]);
            } else {
                target[key] = source[key];
            }
        }
        return target;
    };
    merge(CONFIG, CONFIG_LOCAL);
}

/**
 * Validate configuration
 */
if (!CONFIG.api.baseUrl) {
    console.error('Configuration error: api.baseUrl is required');
}

// Export for use in the application
const API_BASE = CONFIG.api.baseUrl;
const APP_DEBUG = CONFIG.debug;
const APP_ENVIRONMENT = CONFIG.environment;
