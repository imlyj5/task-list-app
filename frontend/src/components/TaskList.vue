<template>
  <ul class="tasks-list">
    <Task
      v-for="task in tasks"
      :key="task.id"
      :task="task"
      @toggle-task-presence="onToggleTaskPresence"
      @delete-task="onDeleteTask"
    />
  </ul>
</template>

<script setup lang="ts">
// List of tasks using the Task component.
// Props: an array of task objects to display
// Emits:
//   - toggleTaskPresence: when a task is toggled complete/incomplete
//   - deleteTask: when a task is deleted
import Task from './Task.vue'
import type { Task as TaskType } from '@/types'
import { api } from '@/services/api'
import { fetchGoals } from '@/stores/goals'

interface Props {
  tasks: TaskType[]
}

defineProps<Props>()

const emit = defineEmits<{
  toggleTaskPresence: [id: number]
  deleteTask: [id: number]
}>()

const onToggleTaskPresence = async (id: number) => {
  await api.toggleTaskPresenceApi(id, isComplete)
  await fetchGoals()
}

const onDeleteTask = (id: number) => {
  emit('deleteTask', id)
}
</script>

<style scoped>
.tasks-list {
  list-style: none;
  padding: 0;
  margin: 2rem auto 0 auto;
  max-width: 420px;
  width: 100%;
}
</style> 