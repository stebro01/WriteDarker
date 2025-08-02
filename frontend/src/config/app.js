// Application configuration
// This file contains default configuration values that can be overridden by environment variables

export const AppConfig = {
  // Minimum screen dimensions required for the application
  MIN_WIDTH: parseInt(import.meta.env.VITE_MIN_WIDTH || '1024', 10),
  MIN_HEIGHT: parseInt(import.meta.env.VITE_MIN_HEIGHT || '768', 10),
  
  // Other app configuration can go here
  APP_NAME: 'WriteDarker',
  VERSION: '1.0.0'
}

export default AppConfig