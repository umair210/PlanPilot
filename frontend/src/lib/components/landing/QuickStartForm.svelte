<script lang="ts">
  import Field from "$lib/components/ui/Field.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import "$lib/components/ui/Inputs.css";

  import { createGoal, generatePlan } from "$lib/api/goals";
  import { setGoalCache } from "$lib/stores/goalCache";
  import type {
    ExperienceLevel,
    PlanStyle,
    GoalCreateRequest,
  } from "$lib/types/models";
  import { goto } from "$app/navigation";

  let title = "";
  let description = "";
  let deadline: string | null = null;
  let hours_per_week: number | null = 10;
  let experience_level: ExperienceLevel = "intermediate";
  let style: PlanStyle = "fast_mvp";

  let isLoading = false;
  let errorMsg: string | null = null;
  let isMissingRequired = true;

  $: isMissingRequired =
    title.trim().length === 0 || description.trim().length === 0;

  async function onGenerate() {
    errorMsg = null;
    if (isMissingRequired) {
      errorMsg = "Title and description are required.";
      return;
    }
    isLoading = true;

    try {
      const payload: GoalCreateRequest = {
        title: title.trim(),
        description: description.trim(),
        deadline,
        hours_per_week,
        experience_level,
        style,
      };

      const goal = await createGoal(payload);
      const plan = await generatePlan(goal.id, false);
      setGoalCache(plan);

      await goto(`/goals/${goal.id}`);
    } catch (e: any) {
      errorMsg = e?.detail
        ? JSON.stringify(e.detail)
        : (e?.message ?? "Failed to generate plan");
    } finally {
      isLoading = false;
    }
  }

</script>

<div class="wrap">
  <div class="head">
    <div class="title">Quick start</div>
    <div class="sub muted">Generate a plan in seconds.</div>
  </div>

  {#if errorMsg}
    <div class="error">{errorMsg}</div>
  {/if}

  <div class="grid">
    <Field label="Goal title">
      <input
        class="input"
        bind:value={title}
        placeholder="e.g. Ship PlanPilot MVP"
        required
      />
    </Field>

    <Field label="Deadline (optional)">
      <input
        class="input"
        type="date"
        on:change={(e) =>
          (deadline = (e.target as HTMLInputElement).value || null)}
      />
    </Field>

    <Field label="Hours/week">
      <input
        class="input"
        type="number"
        min="1"
        max="80"
        value={hours_per_week ?? ""}
        on:input={(e) => {
          const v = (e.target as HTMLInputElement).value;
          hours_per_week = v === "" ? null : Number(v);
        }}
      />
    </Field>

    <Field label="Style">
      <select class="select" bind:value={style}>
        <option value="fast_mvp">Fast MVP</option>
        <option value="balanced">Balanced</option>
        <option value="high_quality">High quality</option>
      </select>
    </Field>

    <Field label="Experience">
      <select class="select" bind:value={experience_level}>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>
    </Field>

    <div class="spanAll">
      <Field label="Description">
        <textarea
          class="textarea"
          bind:value={description}
          placeholder="e.g. Build a FastAPI + Svelte app that turns a goal into phases and tasks with estimates and progress tracking."
          rows="4"
          required
        />
      </Field>
    </div>
  </div>

  <div class="actions">
    <Button
      variant="primary"
      size="sm"
      on:click={onGenerate}
      disabled={isLoading || isMissingRequired}
    >
      {#if isLoading}Generating…{:else}Generate plan{/if}
    </Button>
  </div>
</div>

<style>
  .wrap {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .head .title {
    font-weight: 900;
    letter-spacing: -0.02em;
  }
  .head .sub {
    margin-top: 2px;
    font-size: 0.95rem;
  }

  .grid {
    display: grid;
    grid-template-columns: 1.4fr 0.7fr 0.7fr 0.8fr 0.8fr;
    gap: 12px;
  }

  .spanAll {
    grid-column: 1 / -1;
  }

  .actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  .error {
    border: 1px solid rgba(255, 140, 0, 0.35);
    background: rgba(255, 140, 0, 0.09);
    padding: 10px 12px;
    border-radius: 12px;
    white-space: pre-wrap;
    font-size: 13px;
  }

  @media (max-width: 900px) {
    .grid {
      grid-template-columns: 1fr;
    }
  }
</style>
