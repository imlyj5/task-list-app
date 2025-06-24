import axios from 'axios'
import type { Goal } from '@/types'

const API_BASE_URL = '/api'

export const getAllGoalsApi = async (): Promise<Goal[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/goals/`)
    return response.data.results || response.data
  } catch (error) {
    console.log('error:', error)
    return []
  }
} 