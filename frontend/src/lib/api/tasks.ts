import { apiRequest } from "./http";
import type { Task, TaskPatchRequest } from "$lib/types/models";

export function patchTask(taskId: string, payload: TaskPatchRequest): Promise<Task> {
  return apiRequest<Task>(`/api/v1/tasks/${taskId}`, { method: "PATCH", body: payload });
}

export function deleteTask(taskId: string): Promise<{ deleted: boolean }> {
  return apiRequest<{ deleted: boolean }>(`/api/v1/tasks/${taskId}`, { method: "DELETE" });
}

// If your backend already has POST /api/v1/tasks
export function createTask(payload: {
  goal_id: string;
  phase_id?: string | null;
  title: string;
  description: string;
  estimate_minutes: number;
  priority: number;
}): Promise<Task> {
  return apiRequest<Task>(`/api/v1/tasks`, { method: "POST", body: payload });
}
