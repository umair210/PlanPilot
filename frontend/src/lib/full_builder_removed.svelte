<!-- Deprecated: full builder removed. -->
<script lang="ts">
  import AppShell from "$lib/components/layout/AppShell.svelte";
  import Card from "$lib/components/ui/Card.svelte";
  import Field from "$lib/components/ui/Field.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import "$lib/components/ui/Inputs.css";

  import { createGoal, generatePlan } from "$lib/api/goals";
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

  let isSubmitting = false;
  let errorMsg: string | null = null;

  async function onSubmit() {
    errorMsg = null;
    isSubmitting = true;

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
      await generatePlan(goal.id, false);
      await goto(`/goals/${goal.id}`);
    } catch (e: any) {
      errorMsg = e?.detail
        ? JSON.stringify(e.detail)
        : (e?.message ?? "Failed to create goal");
    } finally {
      isSubmitting = false;
    }
  }
</script>

<AppShell title="Create a goal">
  <Card padding="lg">
    <div class="stack">
      <p class="muted">
        Describe what you want to achieve. We’ll generate phases + tasks you can
        execute.
      </p>

      {#if errorMsg}
        <div class="error">{errorMsg}</div>
      {/if}

      <form class="form" on:submit|preventDefault={onSubmit}>
        <Field label="Title">
          <input
            class="input"
            bind:value={title}
            placeholder="e.g. Build an MVP in one weekend"
          />
        </Field>

        <Field label="Description">
          <textarea class="textarea" bind:value={description} rows="6" />
        </Field>

        <div class="row">
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
        </div>

        <div class="row">
          <Field label="Experience">
            <select class="select" bind:value={experience_level}>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </Field>

          <Field label="Style">
            <select class="select" bind:value={style}>
              <option value="fast_mvp">Fast MVP</option>
              <option value="balanced">Balanced</option>
              <option value="high_quality">High quality</option>
            </select>
          </Field>
        </div>

        <div class="actions">
          <Button variant="primary" type="submit" disabled={isSubmitting}>
            {#if isSubmitting}Generating…{:else}Generate plan{/if}
          </Button>
          <Button variant="ghost" on:click={() => goto("/")}>Back</Button>
        </div>
      </form>
    </div>
  </Card>
</AppShell>

<style>
  .stack {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .form {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin-top: 8px;
  }
  .row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  .actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 6px;
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
    .row {
      grid-template-columns: 1fr;
    }
  }
</style>
