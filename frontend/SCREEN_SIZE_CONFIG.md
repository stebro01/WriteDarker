# Screen Size Configuration

## Overview
WriteDarker includes minimum screen dimension requirements (width and height) to ensure optimal user experience across different devices.

## Configuration

### Default Settings
- **Minimum Width**: 1024px (default)
- **Minimum Height**: 768px (default)
- **Fallback**: If no configuration is provided, defaults to 1024×768px

### Setting Custom Minimum Dimensions

#### Option 1: Environment Variable (Recommended)
Create a `.env` file in the frontend directory:
```bash
# frontend/.env
VITE_MIN_WIDTH=1000
VITE_MIN_HEIGHT=800
```

#### Option 2: Direct Configuration
Modify `frontend/src/config/app.js`:
```javascript
export const AppConfig = {
  MIN_WIDTH: 1200, // Change this value
  MIN_HEIGHT: 900, // Change this value
  // ...
}
```

## Behavior

### Screen Size Check
- The application checks screen dimensions on:
  - Initial page load
  - Window resize events
  
### Error Handling
- If screen width < minimum width OR screen height < minimum height:
  - User is redirected to `/error-screen-size`
  - Shows current dimensions vs required dimensions
  - Displays individual progress bars for width and height
  - Visual indicators (✓/✗) for each dimension requirement
  - Provides instructions to resolve the issue
  - Includes a "Check Again" button for re-validation

### Supported Pages
- **ProjectPage.vue**: Includes screen size checking for both dimensions
- **ErrorScreenSize.vue**: Dedicated error page with comprehensive dimension feedback

## Technical Details

- Uses Vue 3 Composition API with computed properties
- Reactive screen dimension monitoring (width & height)
- Individual validation for each dimension
- Automatic cleanup of event listeners
- Router-based navigation for error handling
- Responsive design with Tailwind CSS
- Real-time progress indicators

## Testing

To test the functionality:
1. Set `VITE_MIN_WIDTH` to a high value (e.g., 2000) and/or `VITE_MIN_HEIGHT` to a high value (e.g., 1200)
2. Reload the application
3. Verify redirection to error screen
4. Check individual dimension indicators and progress bars
5. Resize window to meet both requirements
6. Click "Check Again" to return to application