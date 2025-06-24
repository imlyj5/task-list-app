import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Task, CreateTaskRequest } from '@/types'
import * as taskApi from '@/api/tasks'
import { toggleTaskPresenceApi } from '@/api/tasks'

// Pinia store for managing tasks
export const useTaskStore = defineStore('tasks', () => {
  // State: all tasks
  const taskData = ref<Task[]>([])

  // Getters: derived state for completed/incomplete tasks and count
  const completedTasks = computed(() => taskData.value.filter(task => task.is_complete))
  const incompleteTasks = computed(() => taskData.value.filter(task => !task.is_complete))
  const taskCount = computed(() => taskData.value.length)

  // Actions: fetch, toggle, delete, and post tasks
  // Fetch all tasks from the API
  const getAllTasks = async () => {
    const tasks = await taskApi.getAllTasksApi()
    taskData.value = tasks
  }

  // Toggle a task's completion status
  const toggleTaskPresence = async (id: number) => {
    const task = taskData.value.find(task => task.id === id)
    if (!task) return

    const taskStatus = await taskApi.toggleTaskPresenceApi(id, task.is_complete)
    if (taskStatus) {
      taskData.value = taskData.value.map(task =>
        task.id === taskStatus.id ? taskStatus : task
      )
    }
  }

  // Delete a task by ID
  const deleteTask = async (id: number) => {
    await taskApi.deleteTaskApi(id)
    taskData.value = taskData.value.filter(task => task.id !== id)
  }

  // Post a new task to the API
  const postTask = async (task: CreateTaskRequest) => {
    const newTask = await taskApi.postTaskApi(task)
    if (newTask) {
      taskData.value.push(newTask)
    }
  }

  // Expose state, getters, and actions
  return {
    taskData,
    completedTasks,
    incompleteTasks,
    taskCount,
    getAllTasks,
    toggleTaskPresence,
    deleteTask,
    postTask
  }
}) 