import axios from 'axios'
import type { Task, CreateTaskRequest, UpdateTaskRequest, TaskResponse } from '@/types'

const API_BASE_URL = '/api'

// Convert from API format to frontend format
const convertFromApi = (apiTask: any): Task => {
  const { id, title, completed_at, is_complete, goal_id, goal_title, created_at, updated_at } = apiTask
  return { 
    id, 
    title, 
    completed_at, 
    is_complete,
    goal_id,
    goal_title,
    created_at,
    updated_at
  }
}

// getAllTasksApi
export const getAllTasksApi = async (): Promise<Task[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/tasks/`)
    return response.data.results.map(convertFromApi)
  } catch (error) {
    console.log("error:", error)
    return []
  }
}

// postTaskApi
export const postTaskApi = async (task: CreateTaskRequest): Promise<Task | null> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/tasks/`, {
      title: task.title,
      goal_id: task.goal_id
    })
    return convertFromApi(response.data.task)
  } catch (error) {
    console.log("error:", error)
    return null
  }
}

// toggleTaskPresenceApi
export const toggleTaskPresenceApi = async (id: number, isComplete: boolean): Promise<Task | null> => {
  const path = isComplete ? 'mark_incomplete' : 'mark_complete'
  const response = await axios.patch(`${API_BASE_URL}/tasks/${id}/${path}/`)
  return response.data.task
}

// deleteTaskApi
export const deleteTaskApi = async (id: number): Promise<void> => {
  try {
    await axios.delete(`${API_BASE_URL}/tasks/${id}/`)
  } catch (error) {
    console.log("error:", error)
  }
}

// updateTaskApi
export const updateTaskApi = async (id: number, task: UpdateTaskRequest): Promise<Task | null> => {
  try {
    const response = await axios.put(`${API_BASE_URL}/tasks/${id}/`, task)
    return convertFromApi(response.data)
  } catch (error) {
    console.log("error:", error)
    return null
  }
}

// getTaskApi
export const getTaskApi = async (id: number): Promise<Task | null> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/tasks/${id}/`)
    return convertFromApi(response.data.task)
  } catch (error) {
    console.log("error:", error)
    return null
  }
} 