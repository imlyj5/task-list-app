<template>
  <li class="task-card">
    <span
      class="task-title"
      :class="{ completed: task.is_complete }"
      @click="toggleTask"
      >{{ task.title }}</span>
    <button class="delete-btn" @click="$emit('deleteTask', task.id)">x</button>
  </li>
</template>

<script setup lang="ts">
// Single task with its title and delete button.
// Props: the task object to display
import type { Task } from '@/types'

interface Props {
  task: Task
}

const props = defineProps<Props>()
const { task } = props

const emit = defineEmits<{
  toggleTaskPresence: [id: number]
  deleteTask: [id: number]
}>()

const toggleTask = () => {
  emit('toggleTaskPresence', task.id)
}
</script>

<style scoped>
.task-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #DF8ED1;
  border: 4px solid #5D76C9;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(33, 154, 154, 0.08);
  padding: 1.1rem 1.5rem;
  margin-bottom: 1.2rem;
  font-size: 1.25rem;
  font-weight: 500;
  color: #1A1B1C;
  transition: box-shadow 0.2s;
}

.task-title {
  color: #1A1B1C;
  font-size: 1.15em;
  font-weight: 500;
  letter-spacing: 0.2px;
  cursor: pointer;
  transition: color 0.15s;
  font-family: "Montserrat", sans-serif;
}
.task-title.completed {
  text-decoration: line-through;
  color: #94911C;
}

.delete-btn {
  background: #F06115;
  border: none;
  color: #FFFBF7;
  font-size: 1.3rem;
  font-weight: bold;
  cursor: pointer;
  padding: 0.2em 0.7em;
  border-radius: 50%;
  transition: background 0.15s;
}
.delete-btn:hover {
  background: #5D76C9;
  color: #FFFBF7;
}
</style> 