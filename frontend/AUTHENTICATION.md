# WriteDarker Frontend Authentication System

## Overview

A complete authentication system built with Vue 3, Quasar, Pinia, and Tailwind CSS featuring a beautiful orange-themed UI.

## Features

- ✅ User registration and login
- ✅ JWT token-based authentication
- ✅ Protected routing with route guards
- ✅ Persistent session with localStorage
- ✅ Automatic session restoration
- ✅ Orange-themed UI components
- ✅ Responsive design
- ✅ Form validation
- ✅ Loading states and error handling

## Architecture

### Stores (Pinia)

#### API Store (`src/stores/api.js`)
- Centralized HTTP client with axios
- Automatic token handling
- Error handling and loading states
- Authentication endpoints

#### User Store (`src/stores/user.js`)
- User state management
- Authentication actions (login, register, logout)
- Session persistence
- User profile management

### Components

#### UI Components (`src/components/ui/`)
- `BaseButton.vue` - Customizable button with orange theme
- `BaseInput.vue` - Form input with validation support
- `BaseCard.vue` - Flexible card component
- `BaseModal.vue` - Modal dialog component

### Pages

#### Auth Page (`src/pages/AuthPage.vue`)
- Combined login/register form
- Beautiful orange gradient background
- Form validation
- Animated blob decorations

#### Dashboard Page (`src/pages/DashboardPage.vue`)
- Protected dashboard view
- User profile display
- Status indicators
- Quick action buttons

### Routing

#### Route Guards (`src/router/auth-guard.js`)
- `authGuard` - Protects authenticated routes
- `guestGuard` - Redirects authenticated users

#### Routes (`src/router/routes.js`)
- `/` - Redirects to dashboard
- `/auth` - Login/register page (guest only)
- `/dashboard` - Protected dashboard (auth required)

## Usage

### Starting the Development Server

```bash
cd frontend
npm run dev
```

### API Configuration

The frontend expects the backend API to be running on `http://localhost:8000` by default. You can configure this with the `VITE_API_URL` environment variable.

### Backend API Endpoints Used

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me?token={token}` - Get current user
- `PUT /auth/me?token={token}` - Update user profile
- `POST /auth/logout` - Logout (placeholder)

## Styling

The UI uses a beautiful orange color scheme throughout:
- Primary: Orange-500 (#f97316)
- Hover: Orange-600 (#ea580c)
- Background gradients: Orange-50 to Orange-100
- Consistent spacing and typography

## Security Features

- JWT tokens stored in localStorage
- Automatic token validation
- Route-level authentication guards
- Session restoration on page reload
- Proper error handling for expired tokens