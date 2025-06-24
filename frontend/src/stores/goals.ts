import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Goal } from '@/types'
import { getAllGoalsApi } from '@/api/goals'

// Pinia store for managing goals
export const useGoalStore = defineStore('goals', () => {
  // State: all goals
  const goals = ref<Goal[]>([])

  // Action: fetch all goals from the API
  const fetchGoals = async () => {
    const fetchedGoals = await getAllGoalsApi()
    // Force reactivity by creating a new array reference
    goals.value = [...fetchedGoals]
  }

  // Expose state and actions
  return { goals, fetchGoals }
}) 