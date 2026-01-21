import { apiRequest } from "./http";
import type { Goal, GoalCreateRequest, GoalDetailResponse } from "$lib/types/models";

export function createGoal(payload: GoalCreateRequest): Promise<Goal> {
  return apiRequest<Goal>("/api/v1/goals", { method: "POST", body: payload });
}

export function getGoal(goalId: string): Promise<GoalDetailResponse> {
  return apiRequest<GoalDetailResponse>(`/api/v1/goals/${goalId}`, { method: "GET" });
}

export function generatePlan(goalId: string, force = false): Promise<GoalDetailResponse> {
  return apiRequest<GoalDetailResponse>(`/api/v1/goals/${goalId}/generate?force=${force}`, {
    method: "POST",
  });
}
