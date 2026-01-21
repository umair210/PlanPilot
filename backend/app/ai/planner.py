import json
import math
from datetime import date
from fastapi import HTTPException
from pydantic import ValidationError

from app.ai.clients import get_openai_client  # keep your import as-is
from app.ai.prompts import (
    plan_system_prompt,
    build_plan_user_prompt,
    rephrase_system_prompt,
    build_rephrase_user_prompt,
)
from app.schemas.ai import AIPlan, AIRephrasedGoal
from app.core.config import settings


def _enforce_no_additional_properties(schema: object) -> object:
    """
    OpenAI Structured Outputs strict schemas require:
    - every object schema must include: additionalProperties: false
    We apply this recursively to all sub-schemas.
    """
    if isinstance(schema, dict):
        if schema.get("type") == "object":
            schema["additionalProperties"] = False

            props = schema.get("properties")
            if isinstance(props, dict):
                # Helps strict validation (keeps output predictable)
                schema["required"] = list(props.keys())

        for k, v in list(schema.items()):
            schema[k] = _enforce_no_additional_properties(v)

    elif isinstance(schema, list):
        for i in range(len(schema)):
            schema[i] = _enforce_no_additional_properties(schema[i])

    return schema


def _ai_plan_text_format() -> dict:
    """
    Responses API uses: text={ "format": {...} }
    NOT response_format=...
    """
    raw = AIPlan.model_json_schema()
    if raw.get("type") is None:
        raw["type"] = "object"

    strict_schema = _enforce_no_additional_properties(raw)

    return {
        "type": "json_schema",
        "name": "planpilot_plan",
        "strict": True,
        "schema": strict_schema,
    }


def _ai_rephrase_text_format() -> dict:
    raw = AIRephrasedGoal.model_json_schema()
    if raw.get("type") is None:
        raw["type"] = "object"

    strict_schema = _enforce_no_additional_properties(raw)

    return {
        "type": "json_schema",
        "name": "planpilot_goal_rephrase",
        "strict": True,
        "schema": strict_schema,
    }


def _parse_deadline(deadline) -> date | None:
    if deadline is None:
        return None
    if isinstance(deadline, date):
        return deadline
    if isinstance(deadline, str):
        try:
            return date.fromisoformat(deadline)
        except ValueError:
            return None
    return None


def _total_available_minutes(deadline, hours_per_week) -> int | None:
    if not deadline or hours_per_week is None:
        return None
    deadline_date = _parse_deadline(deadline)
    if not deadline_date:
        return None

    delta_days = (deadline_date - date.today()).days
    if delta_days < 0:
        return 0

    days_available = max(delta_days, 1)
    total_hours = hours_per_week * (days_available / 7)
    return int(math.ceil(total_hours * 60))


def _plan_total_minutes(plan: AIPlan) -> int:
    return sum(task.estimate_minutes for phase in plan.phases for task in phase.tasks)


def _trim_plan_to_budget(plan: AIPlan, total_available_minutes: int) -> AIPlan:
    total_minutes = _plan_total_minutes(plan)
    if total_minutes <= total_available_minutes:
        return plan

    remaining_tasks = sum(len(phase.tasks) for phase in plan.phases)
    candidates = []
    for phase in plan.phases:
        for task in phase.tasks:
            candidates.append((phase, task))

    candidates.sort(
        key=lambda item: (item[1].priority, item[1].estimate_minutes),
        reverse=True,
    )

    for phase, task in candidates:
        if total_minutes <= total_available_minutes:
            break
        if remaining_tasks <= 1:
            break
        phase.tasks.remove(task)
        remaining_tasks -= 1
        total_minutes -= task.estimate_minutes

    plan.phases = [phase for phase in plan.phases if phase.tasks]
    return plan


def _apply_time_budget(plan: AIPlan, total_available_minutes: int | None) -> AIPlan:
    if not total_available_minutes or total_available_minutes <= 0:
        return plan
    return _trim_plan_to_budget(plan, total_available_minutes)


async def rephrase_goal_input(
    *,
    title: str,
    description: str,
    deadline,
    hours_per_week,
    experience_level: str,
    style: str,
) -> dict:
    if not settings.OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    client = get_openai_client()

    sys = rephrase_system_prompt()
    user = build_rephrase_user_prompt(
        title=title,
        description=description,
        deadline=deadline,
        hours_per_week=hours_per_week,
        experience_level=experience_level,
        style=style,
    )

    try:
        resp = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {"role": "system", "content": sys},
                {"role": "user", "content": user},
            ],
            text={"format": _ai_rephrase_text_format()},
        )
        data = json.loads(resp.output_text)
        return AIRephrasedGoal.model_validate(data).model_dump()
    except (json.JSONDecodeError, ValidationError):
        pass
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI call failed: {e}")

    try:
        resp2 = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {"role": "system", "content": sys},
                {"role": "user", "content": user},
                {"role": "user", "content": "Fix the JSON to match the schema exactly. Return JSON only."},
            ],
            text={"format": _ai_rephrase_text_format()},
        )
        data2 = json.loads(resp2.output_text)
        return AIRephrasedGoal.model_validate(data2).model_dump()
    except Exception:
        raise HTTPException(status_code=422, detail="AI output could not be validated after retry")


async def generate_plan(*, title: str, description: str, deadline, hours_per_week, experience_level: str, style: str) -> AIPlan:
    if not settings.OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    client = get_openai_client()

    sys = plan_system_prompt()
    total_available_minutes = _total_available_minutes(deadline, hours_per_week)
    user = build_plan_user_prompt(
        title=title,
        description=description,
        deadline=deadline,
        hours_per_week=hours_per_week,
        experience_level=experience_level,
        style=style,
        total_available_minutes=total_available_minutes,
    )

    # 1) First attempt
    try:
        resp = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {"role": "system", "content": sys},
                {"role": "user", "content": user},
            ],
            text={"format": _ai_plan_text_format()},
        )
        data = json.loads(resp.output_text)
        return _apply_time_budget(AIPlan.model_validate(data), total_available_minutes)

    except (json.JSONDecodeError, ValidationError):
        pass
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI call failed: {e}")

    # 2) Repair attempt
    try:
        resp2 = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {"role": "system", "content": sys},
                {"role": "user", "content": user},
                {"role": "user", "content": "Fix the JSON to match the schema exactly. Return JSON only."},
            ],
            text={"format": _ai_plan_text_format()},
        )
        data2 = json.loads(resp2.output_text)
        return _apply_time_budget(AIPlan.model_validate(data2), total_available_minutes)

    except Exception:
        raise HTTPException(status_code=422, detail="AI output could not be validated after retry")
