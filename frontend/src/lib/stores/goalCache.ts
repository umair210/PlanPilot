import { get, writable } from "svelte/store";
import type { GoalDetailResponse } from "$lib/types/models";

const goalCache = writable<GoalDetailResponse | null>(null);

export function setGoalCache(data: GoalDetailResponse) {
  goalCache.set(data);
}

export function takeGoalCache(goalId: string): GoalDetailResponse | null {
  const cached = get(goalCache);
  if (cached && cached.goal.id === goalId) {
    goalCache.set(null);
    return cached;
  }

  return null;
}
