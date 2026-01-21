<script lang="ts">
  export let padding: "md" | "lg" = "lg";
</script>

<div class={`card ${padding}`}>
  <slot />
</div>

<style>
  .card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    backdrop-filter: var(--blur);
    box-shadow: var(--shadow);
  }
  .card.lg {
    padding: 18px;
  }
  .card.md {
    padding: 14px;
  }
</style>
