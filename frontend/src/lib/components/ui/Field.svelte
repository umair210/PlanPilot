<script lang="ts">
  export let label = "";
  export let hint: string | null = null;
</script>

<label class="field">
  <span class="label">{label}</span>
  <slot />
  {#if hint}
    <span class="hint">{hint}</span>
  {/if}
</label>

<style>
  .field {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .label {
    font-size: 12px;
    opacity: 0.78;
    color: var(--muted);
  }
  .hint {
    font-size: 12px;
    opacity: 0.7;
    color: var(--muted);
    margin-top: 2px;
  }
</style>
