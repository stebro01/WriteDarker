<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-white to-orange-100 flex items-center justify-center p-4">
    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-orange-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
      <div class="absolute top-40 left-40 w-80 h-80 bg-orange-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Auth container -->
    <div class="relative w-full max-w-md">
      <BaseCard variant="glass" padding="none">
        <!-- Header with logo/brand -->
        <div class="text-center px-6 pt-8 pb-2">
          <div class="w-16 h-16 bg-gradient-to-r from-orange-400 to-orange-600 rounded-full mx-auto mb-4 flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.828 2.828 0 114 4L9 19.5l-4.5-1L9 14.5z"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-2">WriteDarker</h2>
          <p class="text-gray-600 text-sm">{{ isLogin ? 'Welcome back!' : 'Create your account' }}</p>
        </div>

        <!-- Tab switcher -->
        <div class="px-6 pb-6">
          <div class="flex bg-gray-100 rounded-lg p-1 mb-6">
            <button
              @click="() => { isLogin = true; clearErrors() }"
              :class="[
                'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all duration-200',
                isLogin 
                  ? 'bg-white text-orange-600 shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              Sign In
            </button>
            <button
              @click="() => { isLogin = false; clearErrors() }"
              :class="[
                'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all duration-200',
                !isLogin 
                  ? 'bg-white text-orange-600 shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              Sign Up
            </button>
          </div>

          <!-- Login Form -->
          <form v-if="isLogin" @submit.prevent="handleLogin" class="space-y-4">
            <BaseInput
              v-model="loginForm.username"
              label="Username"
              type="text"
              placeholder="Enter your username"
              required
              autocomplete="username"
              :error="errors.username"
            >
              <template #prepend>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </template>
            </BaseInput>

            <BaseInput
              v-model="loginForm.password"
              label="Password"
              type="password"
              placeholder="Enter your password"
              required
              autocomplete="current-password"
              :error="errors.password"
            >
              <template #prepend>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </template>
            </BaseInput>

            <BaseButton
              type="submit"
              variant="primary"
              size="lg"
              full-width
              :loading="userStore.loading"
              loading-text="Signing in..."
            >
              Sign In
            </BaseButton>
          </form>

          <!-- Register Form -->
          <form v-else @submit.prevent="handleRegister" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <BaseInput
                v-model="registerForm.first_name"
                label="First Name"
                type="text"
                placeholder="John"
                autocomplete="given-name"
                :error="errors.first_name"
              />
              <BaseInput
                v-model="registerForm.last_name"
                label="Last Name"
                type="text"
                placeholder="Doe"
                autocomplete="family-name"
                :error="errors.last_name"
              />
            </div>

            <BaseInput
              v-model="registerForm.username"
              label="Username"
              type="text"
              placeholder="Choose a username"
              required
              autocomplete="username"
              :error="errors.username"
            >
              <template #prepend>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </template>
            </BaseInput>

            <BaseInput
              v-model="registerForm.email"
              label="Email"
              type="email"
              placeholder="john@example.com"
              autocomplete="email"
              :error="errors.email"
            >
              <template #prepend>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </template>
            </BaseInput>

            <BaseInput
              v-model="registerForm.age"
              label="Age"
              type="number"
              placeholder="25"
              min="1"
              max="120"
              :error="errors.age"
            >
              <template #prepend>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                </svg>
              </template>
            </BaseInput>

            <BaseInput
              v-model="registerForm.password"
              label="Password"
              type="password"
              placeholder="Create a strong password"
              required
              autocomplete="new-password"
              :error="errors.password"
            >
              <template #prepend>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </template>
            </BaseInput>

            <BaseInput
              v-model="confirmPassword"
              label="Confirm Password"
              type="password"
              placeholder="Confirm your password"
              required
              autocomplete="new-password"
              :error="errors.confirmPassword"
            >
              <template #prepend>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </template>
            </BaseInput>

            <BaseButton
              type="submit"
              variant="primary"
              size="lg"
              full-width
              :loading="userStore.loading"
              loading-text="Creating account..."
            >
              Create Account
            </BaseButton>
          </form>

          <!-- Error message -->
          <div v-if="apiStore.hasError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-600">{{ apiStore.error }}</p>
          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useApiStore } from '../stores/api'
import BaseCard from '../components/ui/BaseCard.vue'
import BaseInput from '../components/ui/BaseInput.vue'
import BaseButton from '../components/ui/BaseButton.vue'

const router = useRouter()
const userStore = useUserStore()
const apiStore = useApiStore()

const isLogin = ref(true)
const confirmPassword = ref('')

const loginForm = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  email: '',
  age: null
})

const errors = reactive({
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  email: '',
  age: '',
  confirmPassword: ''
})

// Clear errors when switching between login/register
const clearErrors = () => {
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })
  apiStore.clearError()
}

// Validate form
const validateLogin = () => {
  clearErrors()
  let isValid = true

  if (!loginForm.username.trim()) {
    errors.username = 'Username is required'
    isValid = false
  }

  if (!loginForm.password) {
    errors.password = 'Password is required'
    isValid = false
  }

  return isValid
}

const validateRegister = () => {
  clearErrors()
  let isValid = true

  if (!registerForm.username.trim()) {
    errors.username = 'Username is required'
    isValid = false
  } else if (registerForm.username.length < 3) {
    errors.username = 'Username must be at least 3 characters'
    isValid = false
  }

  if (!registerForm.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (registerForm.password.length < 6) {
    errors.password = 'Password must be at least 6 characters'
    isValid = false
  }

  if (!confirmPassword.value) {
    errors.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (registerForm.password !== confirmPassword.value) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  if (registerForm.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }

  if (registerForm.age && (registerForm.age < 1 || registerForm.age > 120)) {
    errors.age = 'Please enter a valid age'
    isValid = false
  }

  return isValid
}

// Handle login
const handleLogin = async () => {
  if (!validateLogin()) return

  try {
    await userStore.login(loginForm)
    router.push('/dashboard')
  } catch {
    // Error is handled by the store and displayed via apiStore.error
  }
}

// Handle register
const handleRegister = async () => {
  if (!validateRegister()) return

  try {
    await userStore.register(registerForm)
    router.push('/dashboard')
  } catch {
    // Error is handled by the store and displayed via apiStore.error
  }
}

// Clear errors when switching tabs (functions are called inline in template)

// Redirect if already logged in
onMounted(async () => {
  if (userStore.isLoggedIn) {
    router.push('/dashboard')
  }
})
</script>

<style scoped>
@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}</style>