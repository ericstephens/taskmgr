import axios from 'axios';

// Define the base URL for the API
const API_URL = 'http://localhost:8000';

// Define the Task interface
export interface Task {
  id: number;
  title: string;
  description: string | null;
  due_date: string | null;
  priority: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

// Define the interface for creating a new task
export interface CreateTaskData {
  title: string;
  description?: string;
  due_date?: string;
  priority?: string;
}

// Define the interface for updating a task
export interface UpdateTaskData {
  title?: string;
  description?: string;
  due_date?: string;
  priority?: string;
  completed?: boolean;
}

// Create an axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const getTasks = async (completed?: boolean): Promise<Task[]> => {
  const params = completed !== undefined ? { completed } : {};
  const response = await api.get('/tasks', { params });
  return response.data;
};

export const getTaskById = async (id: number): Promise<Task> => {
  const response = await api.get(`/tasks/${id}`);
  return response.data;
};

export const createTask = async (taskData: CreateTaskData): Promise<Task> => {
  const response = await api.post('/tasks', taskData);
  return response.data;
};

export const updateTask = async (id: number, taskData: UpdateTaskData): Promise<Task> => {
  const response = await api.put(`/tasks/${id}`, taskData);
  return response.data;
};

export const deleteTask = async (id: number): Promise<void> => {
  await api.delete(`/tasks/${id}`);
};

export const markTaskCompleted = async (id: number): Promise<Task> => {
  const response = await api.post(`/tasks/${id}/complete`);
  return response.data;
};

export const markTaskPending = async (id: number): Promise<Task> => {
  const response = await api.post(`/tasks/${id}/pending`);
  return response.data;
};

export default {
  getTasks,
  getTaskById,
  createTask,
  updateTask,
  deleteTask,
  markTaskCompleted,
  markTaskPending,
};
