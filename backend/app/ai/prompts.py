def rephrase_system_prompt() -> str:
    return (
        "You are a goal normalization assistant.\n"
        "Return ONLY valid JSON with the exact keys and structure requested. "
        "No markdown, no extra keys, no commentary.\n\n"
        "Rules:\n"
        "- Preserve meaning; do not invent new requirements.\n"
        "- If deadline is missing, set explicit_constraints.deadline to \"\".\n"
        "- If hours_per_week is missing, set explicit_constraints.hours_per_week to null.\n"
        "- You may always set clarifying_questions to [].\n"
    )


def build_rephrase_user_prompt(
    *,
    title: str,
    description: str,
    deadline,
    hours_per_week,
    experience_level: str,
    style: str,
) -> str:
    deadline_value = deadline or ""
    hours_value = hours_per_week if hours_per_week is not None else "null"
    return f"""
Goal title: {title}
Goal description: {description}

Inputs:
- Deadline: {deadline_value}
- Hours per week: {hours_value}
- Experience level: {experience_level}
- Style: {style}

Return JSON with this exact shape (no extra keys):
{{
  "normalized_title": string,
  "normalized_description": string,
  "explicit_constraints": {{
    "deadline": string,
    "hours_per_week": number|null,
    "experience_level": string,
    "style": string
  }},
  "must_include": string[],
  "avoid": string[],
  "clarifying_questions": string[]
}}
""".strip()


def plan_system_prompt() -> str:
    return (
        "You are an expert project planning assistant.\n"
        "Return ONLY valid JSON that matches the provided schema. "
        "No markdown, no extra keys, no commentary.\n\n"
        "Core rules:\n"
        "- Focus on planning: phases, tasks, estimates, dependencies, acceptance criteria.\n"
        "- Tasks must be executable and specific (one clear action).\n"
        "- Avoid vague tasks like 'Research more' unless it has a concrete output and acceptance criteria.\n"
        "- Ensure feasibility with time constraints: your estimates must fit the deadline and hours/week.\n"
        "- If total_available_minutes is provided, keep Sum(task.estimate_minutes) <= total_available_minutes.\n"
    )


def build_plan_user_prompt(
    *,
    title: str,
    description: str,
    deadline,
    hours_per_week,
    experience_level: str,
    style: str,
    total_available_minutes: int | None,
) -> str:
    time_budget = total_available_minutes if total_available_minutes is not None else "unknown"
    return f"""
Goal title: {title}
Goal description: {description}

Constraints:
- Deadline: {deadline or "none"}
- Time budget (hours/week): {hours_per_week or "unknown"}
- Total available minutes: {time_budget}
- Experience level: {experience_level}
- Style: {style}

Your task is to create a detailed project plan to achieve the goal described above.
Follow these requirements strictly:
-If a deadline is provided, ensure the plan is feasible within that timeframe given the time budget.
-If no deadline is provided, create a reasonable plan based on the time budget.
-If user adds the testing data, ensure the plan includes appropriate testing and validation tasks, and keep the response within the schema with test data

Instructions:
- Break the goal into phases (max 8).
- Adjust the number of phases and tasks based on the time budget.
- Each phase has objective and 1-10 concrete tasks (fewer if time is tight).
- Each task must be executable and specific (not vague).
- Provide estimate_minutes (5..480), priority (1..5), and acceptance_criteria.
""".strip()
