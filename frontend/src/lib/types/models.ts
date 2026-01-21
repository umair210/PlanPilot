export type ExperienceLevel = "beginner" | "intermediate" | "advanced";
export type PlanStyle = "fast_mvp" | "balanced" | "high_quality";
export type TaskStatus = "todo" | "done";

export interface Goal {
  id: string;
  title: string;
  description: string;
  deadline: string | null; // ISO date string
  hours_per_week: number | null;
  experience_level: ExperienceLevel;
  style: PlanStyle;
  created_at: string; // ISO datetime
}

export interface Phase {
  id: string;
  goal_id: string;
  title: string;
  objective: string;
  order_index: number;
}

export interface Task {
  id: string;
  goal_id: string;
  phase_id: string | null;
  parent_task_id: string | null;
  title: string;
  description: string;
  estimate_minutes: number;
  priority: number;
  status: TaskStatus;
  order_index: number;
  created_by: string;
}

export interface GoalDetailResponse {
  goal: Goal;
  phases: Phase[];
  tasks: Task[];
}

export interface GoalCreateRequest {
  title: string;
  description: string;
  deadline: string | null;
  hours_per_week: number | null;
  experience_level: ExperienceLevel;
  style: PlanStyle;
}

export interface TaskPatchRequest {
  title?: string;
  description?: string;
  estimate_minutes?: number;
  priority?: number;
  status?: TaskStatus;
  phase_id?: string | null;
  order_index?: number;
}
