<template>
  <div class="h-screen bg-gray-50 flex flex-col overflow-hidden">
    <!-- Header -->
    <PageHeader 
      title="User Details" 
      :show-back-button="true"
      back-route="/dashboard"
    >
      <template #actions>
        <BaseButton 
          variant="primary" 
          size="sm" 
          @click="saveChanges"
          :disabled="!hasChanges || saving"
        >
          <svg v-if="saving" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </BaseButton>
      </template>
    </PageHeader>

    <!-- Main content -->
    <div class="flex-1 overflow-auto p-6">
      <div class="max-w-2xl mx-auto">
        <!-- Profile Section -->
        <BaseCard variant="elevated" padding="lg" class="mb-6">
          <template #header>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center mr-3">
                <div class="text-lg font-bold text-white">{{ userStore.userInitials }}</div>
              </div>
              <div>
                <h2 class="text-lg font-medium text-gray-900">Profile Information</h2>
                <p class="text-sm text-gray-600">Update your personal details</p>
              </div>
            </div>
          </template>

          <form @submit.prevent="saveChanges" class="space-y-6">
            <!-- First Name -->
            <div>
              <label for="firstName" class="block text-sm font-medium text-gray-700 mb-2">
                First Name
              </label>
              <input
                id="firstName"
                v-model="form.first_name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter your first name"
              />
            </div>

            <!-- Last Name -->
            <div>
              <label for="lastName" class="block text-sm font-medium text-gray-700 mb-2">
                Last Name
              </label>
              <input
                id="lastName"
                v-model="form.last_name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter your last name"
              />
            </div>

            <!-- Email -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter your email address"
              />
            </div>

            <!-- Age -->
            <div>
              <label for="age" class="block text-sm font-medium text-gray-700 mb-2">
                Age
              </label>
              <input
                id="age"
                v-model.number="form.age"
                type="number"
                min="1"
                max="120"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter your age"
              />
            </div>

            <!-- Username (read-only) -->
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                id="username"
                :value="userStore.currentUser?.username"
                type="text"
                disabled
                class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500 cursor-not-allowed"
              />
              <p class="text-xs text-gray-500 mt-1">Username cannot be changed</p>
            </div>
          </form>
        </BaseCard>

        <!-- Account Security Section -->
        <BaseCard variant="elevated" padding="lg">
          <template #header>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-gradient-to-br from-red-400 to-red-600 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
              <div>
                <h2 class="text-lg font-medium text-gray-900">Account Security</h2>
                <p class="text-sm text-gray-600">Manage your account security</p>
              </div>
            </div>
          </template>

          <div class="space-y-4">
            <!-- Password Change -->
            <div class="border border-gray-200 rounded-lg p-4">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-medium text-gray-900">Password</h3>
                  <p class="text-xs text-gray-500">Last changed: Never</p>
                </div>
                <BaseButton variant="outline" size="sm" @click="showPasswordModal = true">
                  Change Password
                </BaseButton>
              </div>
            </div>

            <!-- Account Status -->
            <div class="border border-gray-200 rounded-lg p-4">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-medium text-gray-900">Account Status</h3>
                  <p class="text-xs text-gray-500">Your account is active and secure</p>
                </div>
                <div class="flex items-center">
                  <div class="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                  <span class="text-sm text-green-600 font-medium">Active</span>
                </div>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>
    </div>

    <!-- Password Change Modal -->
    <div v-if="showPasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4" @click.stop>
        <div class="p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Change Password</h3>
          
          <form @submit.prevent="changePassword" class="space-y-4">
            <div>
              <label for="currentPassword" class="block text-sm font-medium text-gray-700 mb-2">
                Current Password
              </label>
              <input
                id="currentPassword"
                v-model="passwordForm.currentPassword"
                type="password"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter current password"
              />
            </div>

            <div>
              <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-2">
                New Password
              </label>
              <input
                id="newPassword"
                v-model="passwordForm.newPassword"
                type="password"
                required
                minlength="6"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter new password"
              />
            </div>

            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
                Confirm New Password
              </label>
              <input
                id="confirmPassword"
                v-model="passwordForm.confirmPassword"
                type="password"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Confirm new password"
              />
            </div>

            <div v-if="passwordForm.newPassword && passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword" class="text-sm text-red-600">
              Passwords do not match
            </div>

            <div class="flex space-x-3 pt-4">
              <BaseButton 
                type="button"
                variant="outline" 
                size="sm" 
                @click="showPasswordModal = false"
                class="flex-1"
              >
                Cancel
              </BaseButton>
              <BaseButton 
                type="submit"
                variant="primary" 
                size="sm" 
                :disabled="!canChangePassword || changingPassword"
                class="flex-1"
              >
                {{ changingPassword ? 'Changing...' : 'Change Password' }}
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '../stores/user'
import BaseCard from '../components/ui/BaseCard.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import PageHeader from '../components/ui/PageHeader.vue'

const userStore = useUserStore()

// Form state
const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  age: null
})

// Password change state
const showPasswordModal = ref(false)
const changingPassword = ref(false)
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Loading state
const saving = ref(false)

// Computed properties
const hasChanges = computed(() => {
  const currentUser = userStore.currentUser
  if (!currentUser) return false
  
  return (
    form.value.first_name !== (currentUser.first_name || '') ||
    form.value.last_name !== (currentUser.last_name || '') ||
    form.value.email !== (currentUser.email || '') ||
    form.value.age !== (currentUser.age || null)
  )
})

const canChangePassword = computed(() => {
  return (
    passwordForm.value.currentPassword &&
    passwordForm.value.newPassword &&
    passwordForm.value.confirmPassword &&
    passwordForm.value.newPassword === passwordForm.value.confirmPassword &&
    passwordForm.value.newPassword.length >= 6
  )
})

// Initialize form with current user data
const initializeForm = () => {
  const currentUser = userStore.currentUser
  if (currentUser) {
    form.value = {
      first_name: currentUser.first_name || '',
      last_name: currentUser.last_name || '',
      email: currentUser.email || '',
      age: currentUser.age || null
    }
  }
}

// Save user changes
const saveChanges = async () => {
  if (!hasChanges.value || saving.value) return
  
  saving.value = true
  try {
    const updateData = {}
    
    // Only include fields that have changed
    if (form.value.first_name !== (userStore.currentUser?.first_name || '')) {
      updateData.first_name = form.value.first_name
    }
    if (form.value.last_name !== (userStore.currentUser?.last_name || '')) {
      updateData.last_name = form.value.last_name
    }
    if (form.value.email !== (userStore.currentUser?.email || '')) {
      updateData.email = form.value.email
    }
    if (form.value.age !== (userStore.currentUser?.age || null)) {
      updateData.age = form.value.age
    }
    
    await userStore.updateProfile(updateData)
    
    // Show success message
    alert('Profile updated successfully!')
  } catch (error) {
    console.error('Error updating profile:', error)
    alert('Failed to update profile. Please try again.')
  } finally {
    saving.value = false
  }
}

// Change password
const changePassword = async () => {
  if (!canChangePassword.value || changingPassword.value) return
  
  changingPassword.value = true
  try {
    await userStore.changePassword(
      passwordForm.value.currentPassword,
      passwordForm.value.newPassword
    )
    
    // Reset form and close modal
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    showPasswordModal.value = false
    
    alert('Password changed successfully!')
  } catch (error) {
    console.error('Error changing password:', error)
    alert('Failed to change password. Please check your current password and try again.')
  } finally {
    changingPassword.value = false
  }
}



onMounted(() => {
  // Ensure user data is loaded
  if (!userStore.currentUser) {
    userStore.fetchCurrentUser()
  }
  initializeForm()
})

// Watch for user data changes
watch(() => userStore.currentUser, initializeForm, { immediate: true })
</script> 