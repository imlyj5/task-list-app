<template>
  <form @submit.prevent="handleSubmit" class="newTaskForm">
    <div>
      <label for="title">Task Name</label>
      <input name="title" id="title" v-model="title" type="text" />
      <label for="goal">Goal Category</label>
      <select id="goal" v-model="selectedGoalId" required>
        <option :value="null" disabled>Select a goal</option>
        <option v-for="goal in goals" :key="goal.id" :value="goal.id">{{ goal.title }}</option>
      </select>
      <button>Add Task</button>
    </div>
  </form>
</template>

<script setup lang="ts">
// This component provides a form to create a new task.
//onPostTask: function to call when a new task is submitted

import { ref, computed } from 'vue'
import type { CreateTaskRequest } from '@/types'
import { useGoalStore } from '@/stores/goals'

const props = defineProps<{
  onPostTask: (task: CreateTaskRequest) => Promise<void>
}>()

const title = ref('')
const selectedGoalId = ref<number | null>(null)

const goalStore = useGoalStore()
const goals = computed(() => goalStore.goals)

const handleSubmit = async () => {
  if (!title.value || !selectedGoalId.value) return
  await props.onPostTask({
    title: title.value,
    goal_id: selectedGoalId.value
  })
  title.value = ''
  selectedGoalId.value = null
}
</script>