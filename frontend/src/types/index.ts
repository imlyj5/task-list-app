export interface Task {
  id: number
  title: string
  completed_at?: string
  is_complete: boolean
  goal_id?: number
  goal_title?: string
  created_at: string
  updated_at: string
}

export interface Goal {
  id: number
  title: string
  tasks: Task[]
  task_count: number
  created_at: string
  updated_at: string
}

export interface CreateTaskRequest {
  title: string
  goal_id?: number
}

export interface CreateGoalRequest {
  title: string
}

export interface UpdateTaskRequest {
  title?: string
}

export interface UpdateGoalRequest {
  title?: string
}

export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

export interface TaskResponse {
  task: Task
}

export interface GoalResponse {
  goal: Goal
}

export interface TasksResponse {
  results: Task[]
  count: number
  next?: string
  previous?: string
}

export interface GoalsResponse {
  results: Goal[]
  count: number
  next?: string
  previous?: string
} 