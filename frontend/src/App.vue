<template>
  <header>
    <div class="logo">
    </div>
  </header>
  <section class="hero">
    <h1>Goals & Tasks</h1>
  </section>
  <div class="marqueeContainer">
    <div class="marquee">
        ✨ Complete a task today and make progress! 🚀 
    </div>
  </div>
  <main>
    <div class="group">
      <div v-for="goal in goalStore.goals" :key="goal.id">
        <GoalSection
          :goal="goal"
          @toggle-task-presence="handleToggleTask"
          @delete-task="handleDeleteTask"
        />
      </div>
      <NewTaskForm :on-post-task="handlePostTask" />
    </div>
  </main>
</template>

<script setup lang="ts">
// Import Vue lifecycle and stores
import { onMounted } from 'vue'
import { useGoalStore } from './stores/goals'
import { toggleTaskPresenceApi, deleteTaskApi, postTaskApi } from './api/tasks'
import GoalSection from './components/GoalSection.vue'
import NewTaskForm from './components/NewTaskForm.vue'

// Initialize stores
const goalStore = useGoalStore()

// When the app loads, fetches all goals from the backend
onMounted(() => {
  goalStore.fetchGoals()
})

// Handle toggling a task's completion status
const handleToggleTask = async (taskId: number) => {
  try {
    // Get the current task to check its completion status
    const goal = goalStore.goals.find(g => g.tasks.some(t => t.id === taskId))
    const task = goal?.tasks.find(t => t.id === taskId)
    
    if (task) {
      await toggleTaskPresenceApi(taskId, task.is_complete)
      await goalStore.fetchGoals() // Refresh goals to update UI
    }
  } catch (error) {
    console.error('Error toggling task:', error)
  }
}

// Handle deleting a task
const handleDeleteTask = async (taskId: number) => {
  try {
    await deleteTaskApi(taskId)
    await goalStore.fetchGoals() // Refresh goals to update UI
  } catch (error) {
    console.error('Error deleting task:', error)
  }
}

// Handle posting a new task
const handlePostTask = async (task: any) => {
  try {
    await postTaskApi(task)
    await goalStore.fetchGoals() // Refresh goals to update UI
  } catch (error) {
    console.error('Error posting task:', error)
  }
}
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

.App {
  text-align: center;
  min-height: 100vh;
  background: linear-gradient(180deg, #219a9a 0%, #3ec6c6 100%);
}

.App-header {
  background: linear-gradient(180deg, #219a9a 0%, #3ec6c6 100%);
  min-height: 120px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 2rem 2rem 1rem 2rem;
  gap: 1rem;
}

.emoji {
  font-size: 2.5rem;
  margin-right: 0.5rem;
}

.App-header h1 {
  margin: 0;
  color: #fff;
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: 1px;
}

main {
  max-width: 800px;
  margin: 0 auto;
}

.App-link {
  color: #61dafb;
}
</style> 