<script lang="ts">
  import AppShell from "$lib/components/layout/AppShell.svelte";
  import Card from "$lib/components/ui/Card.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import type { GoalDetailResponse, Task } from "$lib/types/models";

  export let data: GoalDetailResponse;

  const { goal, phases, tasks } = data;

  const doneCount = tasks.filter((t) => t.status === "done").length;
  const totalCount = tasks.length;
  const progress =
    totalCount === 0 ? 0 : Math.round((doneCount / totalCount) * 100);

  function phaseTasks(phaseId: string): Task[] {
    return tasks.filter((t) => t.phase_id === phaseId);
  }
</script>

<AppShell title={goal.title}>
  <div class="stack">
    <Card padding="lg">
      <p class="muted">{goal.description}</p>

      <div class="progressWrap">
        <div class="meta">
          <span><b>{doneCount}</b> / {totalCount} done</span>
          <span>{progress}%</span>
        </div>
        <div class="bar"><div class="fill" style={`width:${progress}%`} /></div>
      </div>

      <div class="actions">
        <Button
          variant="primary"
          on:click={() => (location.href = `/goals/${goal.id}/tasks`)}
        >
          Open tasks
        </Button>
        <Button variant="ghost" on:click={() => (location.href = `/#quickstart`)}>
          New goal
        </Button>
      </div>
    </Card>

    <div class="sectionHeaderLocal">
      <h2>Phases</h2>
      <p class="muted small">Milestones with task previews.</p>
    </div>

    <div class="grid">
      {#each phases as p}
        <Card padding="lg">
          <div class="phaseHead">
            <div>
              <div class="phaseTitle">{p.title}</div>
              <div class="muted small">{p.objective}</div>
            </div>
            <div class="pill">{phaseTasks(p.id).length} tasks</div>
          </div>

          <ul class="preview">
            {#each phaseTasks(p.id).slice(0, 4) as t}
              <li class:done={t.status === "done"}>{t.title}</li>
            {/each}
          </ul>

          <a class="link" href={`/goals/${goal.id}/tasks?phase=${p.id}`}
            >Manage tasks →</a
          >
        </Card>
      {/each}
    </div>
  </div>
</AppShell>

<style>
  .stack {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 12px;
  }

  .progressWrap {
    margin-top: 14px;
  }
  .meta {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    opacity: 0.92;
    margin-bottom: 8px;
  }
  .bar {
    height: 10px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
  }
  .fill {
    height: 100%;
    background: rgba(255, 255, 255, 0.9);
  }

  .sectionHeaderLocal {
    margin-top: 8px;
  }
  .sectionHeaderLocal h2 {
    font-size: 1.6rem;
    letter-spacing: -0.02em;
  }

  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .phaseHead {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: start;
  }
  .phaseTitle {
    font-weight: 900;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
  }
  .pill {
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 12px;
    opacity: 0.9;
    height: fit-content;
  }

  .preview {
    margin: 12px 0 10px;
    padding-left: 18px;
  }
  .preview li {
    margin: 5px 0;
  }
  .preview li.done {
    text-decoration: line-through;
    opacity: 0.6;
  }

  .link {
    text-decoration: none;
    opacity: 0.9;
  }
  .link:hover {
    text-decoration: underline;
  }

  @media (max-width: 900px) {
    .grid {
      grid-template-columns: 1fr;
    }
  }
</style>
