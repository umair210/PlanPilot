from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.goal import Goal
from app.models.phase import Phase
from app.models.task import Task
from app.ai.planner import generate_plan, rephrase_goal_input


async def generate_plan_for_goal(db: AsyncSession, goal_id: str, force: bool = False):
    goal_res = await db.execute(select(Goal).where(Goal.id == goal_id))
    goal = goal_res.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    goal_data = {
        "title": goal.title,
        "description": goal.description,
        "deadline": goal.deadline,
        "hours_per_week": goal.hours_per_week,
        "experience_level": goal.experience_level,
        "style": goal.style,
    }

    # If not forcing, and phases exist, return existing
    phases_res = await db.execute(select(Phase).where(Phase.goal_id == goal_id))
    existing_phases = list(phases_res.scalars().all())
    if existing_phases and not force:
        tasks_res = await db.execute(select(Task).where(Task.goal_id == goal_id).order_by(Task.order_index))
        return goal, existing_phases, list(tasks_res.scalars().all())

    await db.commit()

    rephrased = await rephrase_goal_input(
        title=goal_data["title"],
        description=goal_data["description"],
        deadline=goal_data["deadline"],
        hours_per_week=goal_data["hours_per_week"],
        experience_level=goal_data["experience_level"],
        style=goal_data["style"],
    )

    plan = await generate_plan(
        title=rephrased["normalized_title"],
        description=rephrased["normalized_description"],
        deadline=goal_data["deadline"],
        hours_per_week=goal_data["hours_per_week"],
        experience_level=goal_data["experience_level"],
        style=goal_data["style"],
    )

    # Persist phases + tasks in one transaction
    task_global_order = 0
    async with db.begin():
        if force or existing_phases:
            tasks_res = await db.execute(select(Task).where(Task.goal_id == goal_id))
            for t in tasks_res.scalars().all():
                await db.delete(t)

            phases_res = await db.execute(select(Phase).where(Phase.goal_id == goal_id))
            for p in phases_res.scalars().all():
                await db.delete(p)

        for p_idx, p in enumerate(plan.phases):
            phase = Phase(
                goal_id=goal_id,
                title=p.title,
                objective=p.objective,
                order_index=p_idx,
            )
            db.add(phase)
            await db.flush()  # get phase.id

            for t in p.tasks:
                task = Task(
                    goal_id=goal_id,
                    phase_id=phase.id,
                    title=t.title,
                    description=t.description + (
                        "\n\nAcceptance criteria:\n- " + "\n- ".join(t.acceptance_criteria)
                        if t.acceptance_criteria else ""
                    ),
                    estimate_minutes=t.estimate_minutes,
                    priority=t.priority,
                    status="todo",
                    order_index=task_global_order,
                    created_by="ai",
                )
                task_global_order += 1
                db.add(task)

    # Refresh collections for return
    phases_res2 = await db.execute(select(Phase).where(Phase.goal_id == goal_id).order_by(Phase.order_index))
    tasks_res2 = await db.execute(select(Task).where(Task.goal_id == goal_id).order_by(Task.order_index))
    return goal, list(phases_res2.scalars().all()), list(tasks_res2.scalars().all())
