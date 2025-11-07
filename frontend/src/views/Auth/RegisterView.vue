<template>
  <div class="card space-y-6">
    <div>
      <h1 class="text-2xl font-semibold">Create your account</h1>
      <p class="text-sm text-gray-500">Get started with a few details.</p>
    </div>
    <form class="space-y-4" @submit.prevent="onSubmit">
      <label class="block">
        <span class="text-sm font-medium">Full name</span>
        <input
          v-model="form.full_name"
          type="text"
          autocomplete="name"
          class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none"
        />
      </label>
      <label class="block">
        <span class="text-sm font-medium">Email</span>
        <input
          v-model="form.email"
          type="email"
          required
          autocomplete="email"
          class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none"
        />
      </label>
      <label class="block">
        <span class="text-sm font-medium">Password</span>
        <input
          v-model="form.password"
          type="password"
          required
          minlength="8"
          autocomplete="new-password"
          class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none"
        />
      </label>
      <button class="btn-primary w-full" :disabled="isLoading">{{ isLoading ? 'Creating account...' : 'Create account' }}</button>
    </form>
    <p class="text-center text-sm text-gray-500">
      Already have an account?
      <RouterLink class="text-primary" to="/login">Sign in</RouterLink>
    </p>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  full_name: '',
  email: '',
  password: '',
})

const isLoading = computed(() => auth.status === 'loading')

const onSubmit = async () => {
  await auth.register({ ...form })
  await router.replace('/dashboard')
}
</script>
