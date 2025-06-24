<template>
  <section class="goal-card">
    <h2 class="goal-title">{{ goal.title }}</h2>
    <ul class="tasks-list">
      <Task
        v-for="task in goal.tasks"
        :key="`${task.id}-${task.is_complete}`"
        :task="task"
        @toggle-task-presence="$emit('toggleTaskPresence', task.id)"
        @delete-task="$emit('deleteTask', task.id)"
      />
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { Goal } from '@/types'
import Task from './Task.vue'

defineProps<{ goal: Goal }>()   //Receives a goal object (with title and tasks).
defineEmits<{  //Declares the events it can emit to the parent
  toggleTaskPresence: [id: number]
  deleteTask: [id: number]
}>()
</script>

<style scoped>
.goal-card {
  background: #5D76C9;
  border-radius: 1.5rem;
  box-shadow: 0 4px 24px rgba(93, 118, 201, 0.15);
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  color: #FFFBF7;
  border: 8px solid #5D76C9;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.goal-title {
  font-size: 2rem;
  font-family: "Bricolage Grotesque", sans-serif;
  color: #DF8ED1;
  margin-bottom: 1.5rem;
  text-shadow:
    -1px -1px 0 #1A1B1C,
    1px -1px 0 #1A1B1C,
    -1px  1px 0 #1A1B1C,
    1px  1px 0 #1A1B1C;
}

.tasks-list {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}
</style> 