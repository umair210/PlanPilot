<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  export let open = false;
  export let title: string | null = null;

  const dispatch = createEventDispatcher<{ close: void }>();

  function close() {
    dispatch("close");
  }

  function onKey(e: KeyboardEvent) {
    if (e.key === "Escape") close();
  }

  onMount(() => {
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });
</script>

{#if open}
  <div class="overlay" on:click={close} role="presentation">
    <div class="modal" on:click|stopPropagation>
      {#if title}
        <div class="head">
          <div class="t">{title}</div>
          <button class="x" on:click={close} aria-label="Close">✕</button>
        </div>
      {/if}
      <div class="body">
        <slot />
      </div>
    </div>
  </div>
{/if}

<style>
  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 200;
    padding: 18px;
  }
  .modal {
    width: min(720px, 100%);
    border-radius: var(--r-lg);
    border: 1px solid var(--border);
    background: rgba(2, 6, 23, 0.78);
    backdrop-filter: var(--blur);
    box-shadow: var(--shadow);
    overflow: hidden;
  }
  .head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }
  .t {
    font-weight: 900;
    letter-spacing: -0.02em;
  }
  .x {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.14);
    color: var(--text);
    border-radius: 10px;
    padding: 6px 10px;
    cursor: pointer;
    opacity: 0.9;
  }
  .x:hover {
    opacity: 1;
  }
  .body {
    padding: 16px;
  }
</style>
