<script lang="ts">
  import Field from "$lib/components/ui/Field.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import "$lib/components/ui/Inputs.css";
  import type { Task } from "$lib/types/models";

  export let task: Task;

  // emits: save(payload), cancel
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher<{
    save: {
      title: string;
      description: string;
      estimate_minutes: number;
      priority: number;
    };
    cancel: void;
  }>();

  let title = task.title;
  let description = task.description;
  let estimate_minutes = task.estimate_minutes;
  let priority = task.priority;

  function submit() {
    dispatch("save", {
      title: title.trim(),
      description: description.trim(),
      estimate_minutes,
      priority,
    });
  }
</script>

<div class="form">
  <Field label="Title">
    <input class="input" bind:value={title} />
  </Field>

  <Field label="Description">
    <textarea class="textarea" rows="6" bind:value={description} />
  </Field>

  <div class="row">
    <Field label="Estimate (minutes)">
      <input
        class="input"
        type="number"
        min="5"
        max="480"
        bind:value={estimate_minutes}
      />
    </Field>

    <Field label="Priority (1-5)">
      <input
        class="input"
        type="number"
        min="1"
        max="5"
        bind:value={priority}
      />
    </Field>
  </div>

  <div class="actions">
    <Button variant="primary" size="sm" on:click={submit}>Save</Button>
    <Button variant="ghost" size="sm" on:click={() => dispatch("cancel")}
      >Cancel</Button
    >
  </div>
</div>

<style>
  .form {
    display: flex;
    flex-direction: column;
    gap: 12px;
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
  @media (max-width: 900px) {
    .row {
      grid-template-columns: 1fr;
    }
  }
</style>
