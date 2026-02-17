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
 * Validate configuration
 */
if (!CONFIG.api.baseUrl) {
    console.error('Configuration error: api.baseUrl is required');
}

// Function to get the current API_BASE (allows dynamic updates after local config loads)
function getAPIBase() {
    return CONFIG.api.baseUrl;
}

// Function to get all config
function getConfig() {
    return CONFIG;
}

// Export individual properties for convenience
const APP_DEBUG = CONFIG.debug;
const APP_ENVIRONMENT = CONFIG.environment;

