<script lang="ts">
  import AppShell from "$lib/components/layout/AppShell.svelte";
  import Card from "$lib/components/ui/Card.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import Modal from "$lib/components/ui/Modal.svelte";
  import { page } from "$app/stores";

  import type { GoalDetailResponse, Task, TaskStatus } from "$lib/types/models";
  import { patchTask } from "$lib/api/tasks";
  import TaskEditor from "$lib/components/tasks/TaskEditor.svelte";

  export let data: GoalDetailResponse;

  let goal = data.goal;
  let phases = data.phases;
  let tasks: Task[] = data.tasks;

  let filter: "all" | TaskStatus = "all";
  let isSaving = false;
  let errorMsg: string | null = null;
  let phaseFilter: string | null = null;
  let taskGroups: { id: string | null; title: string; tasks: Task[] }[] = [];

  // editor state
  let editorOpen = false;
  let activeTask: Task | null = null;

  $: phaseFilter = $page.url.searchParams.get("phase");
  $: filtered =
    filter === "all" ? tasks : tasks.filter((t) => t.status === filter);
  $: filteredByPhase = phaseFilter
    ? filtered.filter((t) => t.phase_id === phaseFilter)
    : filtered;
  $: {
    const groups: { id: string | null; title: string; tasks: Task[] }[] = [];
    const grouped = new Map<string, Task[]>();
    const unassigned: Task[] = [];

    for (const task of filteredByPhase) {
      if (task.phase_id) {
        const list = grouped.get(task.phase_id) ?? [];
        list.push(task);
        grouped.set(task.phase_id, list);
      } else {
        unassigned.push(task);
      }
    }

    for (const phase of phases) {
      const groupTasks = grouped.get(phase.id);
      if (groupTasks && groupTasks.length > 0) {
        groups.push({ id: phase.id, title: phase.title, tasks: groupTasks });
      }
    }

    if (unassigned.length > 0) {
      groups.push({ id: null, title: "Unassigned", tasks: unassigned });
    }

    taskGroups = groups;
  }

  function phaseTitle(phaseId: string | null) {
    if (!phaseId) return "Unassigned";
    return phases.find((p) => p.id === phaseId)?.title ?? "Unknown";
  }

  async function toggleDone(task: Task) {
    errorMsg = null;
    isSaving = true;

    const prev = { ...task };
    task.status = task.status === "done" ? "todo" : "done";
    tasks = [...tasks];

    try {
      const updated = await patchTask(task.id, { status: task.status });
      tasks = tasks.map((t) => (t.id === task.id ? updated : t));
      if (activeTask?.id === task.id) {
        activeTask = updated;
      }
    } catch (e: any) {
      tasks = tasks.map((t) => (t.id === task.id ? prev : t));
      if (activeTask?.id === task.id) {
        activeTask = prev;
      }
      errorMsg = e?.detail
        ? JSON.stringify(e.detail)
        : (e?.message ?? "Failed to update task");
    } finally {
      isSaving = false;
    }
  }

  function openEditor(t: Task) {
    activeTask = t;
    editorOpen = true;
  }

  function closeEditor() {
    editorOpen = false;
    activeTask = null;
  }

  async function saveEdits(
    e: CustomEvent<{
      title: string;
      description: string;
      estimate_minutes: number;
      priority: number;
    }>,
  ) {
    if (!activeTask) return;
    errorMsg = null;
    isSaving = true;

    const taskId = activeTask.id;

    // optimistic UI
    const prev = { ...activeTask };
    activeTask.title = e.detail.title;
    activeTask.description = e.detail.description;
    activeTask.estimate_minutes = e.detail.estimate_minutes;
    activeTask.priority = e.detail.priority;
    tasks = [...tasks];

    try {
      const updated = await patchTask(taskId, {
        title: e.detail.title,
        description: e.detail.description,
        estimate_minutes: e.detail.estimate_minutes,
        priority: e.detail.priority,
      });

      // sync with backend response
      tasks = tasks.map((t) => (t.id === taskId ? updated : t));
      closeEditor();
    } catch (err: any) {
      // rollback
      tasks = tasks.map((t) => (t.id === taskId ? prev : t));
      errorMsg = err?.detail
        ? JSON.stringify(err.detail)
        : (err?.message ?? "Failed to save edits");
    } finally {
      isSaving = false;
    }
  }

  let doneCount = 0;
  $: doneCount = tasks.filter((t) => t.status === "done").length;
</script>

<AppShell title="Tasks">
  <div class="stack">
    <Card padding="lg">
      <div class="top">
        <div>
          <div class="muted small">{goal.title}</div>
          <div class="headline"><b>{doneCount}</b> / {tasks.length} done</div>
        </div>

        <div class="topActions">
          <Button
            variant="ghost"
            size="sm"
            on:click={() => (location.href = `/goals/${goal.id}`)}
          >
            Back to phases
          </Button>
        </div>
      </div>

      <div class="toolbar">
        <div class="filters">
          <button
            class:active={filter === "all"}
            on:click={() => (filter = "all")}>All</button
          >
          <button
            class:active={filter === "todo"}
            on:click={() => (filter = "todo")}>To-do</button
          >
          <button
            class:active={filter === "done"}
            on:click={() => (filter = "done")}>Done</button
          >
        </div>

        {#if isSaving}
          <div class="muted small">Saving…</div>
        {/if}
      </div>

      {#if errorMsg}
        <div class="error">{errorMsg}</div>
      {/if}
    </Card>

    <div class="groupList">
      {#each taskGroups as group (group.id ?? "unassigned")}
        <div class="phaseGroup">
          <div class="phaseHeading">{group.title}</div>

          <div class="taskList">
            {#each group.tasks as t (t.id)}
              <Card padding="lg">
                <div class="row">
                  <input
                    type="checkbox"
                    checked={t.status === "done"}
                    on:change={() => toggleDone(t)}
                  />

                  <div class="body">
                    <div class="titleLine">
                      <div class:done={t.status === "done"} class="title">
                        {t.title}
                      </div>

                      <div class="meta">
                        <span class="chip">{phaseTitle(t.phase_id)}</span>
                        <span class="chip">{t.estimate_minutes}m</span>
                        <span class="chip">P{t.priority}</span>
                      </div>
                    </div>

                    <div class="desc muted small">{t.description}</div>

                    <div class="rowActions">
                      <Button
                        variant="secondary"
                        size="sm"
                        on:click={() => openEditor(t)}>Edit</Button
                      >
                    </div>
                  </div>
                </div>
              </Card>
            {/each}
          </div>
        </div>
      {/each}
    </div>

    <Modal open={editorOpen} title="Edit task" on:close={closeEditor}>
      {#if activeTask}
        <TaskEditor
          task={activeTask}
          on:save={saveEdits}
          on:cancel={closeEditor}
        />
      {/if}
    </Modal>
  </div>
</AppShell>

<style>
  .stack {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .top {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: start;
  }
  .headline {
    font-size: 1.25rem;
    margin-top: 4px;
    letter-spacing: -0.02em;
  }
  .topActions {
    display: flex;
    gap: 10px;
  }

  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    gap: 12px;
    flex-wrap: wrap;
  }

  .filters {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }
  .filters button {
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.04);
    color: var(--text);
    padding: 8px 12px;
    border-radius: 999px;
    cursor: pointer;
    opacity: 0.9;
  }
  .filters button.active {
    border-color: rgba(99, 102, 241, 0.35);
  }

  .groupList {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }
  .phaseGroup {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .phaseHeading {
    font-size: 1.05rem;
    font-weight: 900;
    letter-spacing: -0.02em;
  }
  .taskList {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .row {
    display: flex;
    gap: 12px;
    align-items: start;
  }
  .body {
    flex: 1;
  }

  .titleLine {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    align-items: start;
    flex-wrap: wrap;
  }
  .title {
    font-weight: 900;
    letter-spacing: -0.02em;
  }
  .title.done {
    text-decoration: line-through;
    opacity: 0.65;
  }

  .meta {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    justify-content: flex-end;
  }
  .chip {
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 3px 8px;
    border-radius: 999px;
    font-size: 12px;
    opacity: 0.9;
  }

  .desc {
    margin-top: 8px;
    white-space: pre-wrap;
  }
  .rowActions {
    margin-top: 12px;
    display: flex;
    gap: 10px;
  }

  .error {
    margin-top: 12px;
    border: 1px solid rgba(255, 140, 0, 0.35);
    background: rgba(255, 140, 0, 0.09);
    padding: 10px 12px;
    border-radius: 12px;
    white-space: pre-wrap;
    font-size: 13px;
  }
</style>
