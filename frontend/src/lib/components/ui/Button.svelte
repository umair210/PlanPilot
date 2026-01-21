<script lang="ts">
  // Forward any DOM props + event handlers (on:click, aria-*, etc.)
  export let variant: "primary" | "secondary" | "ghost" = "primary";
  export let size: "md" | "sm" = "md";
  export let type: "button" | "submit" = "button";
  export let disabled = false;

  // Important for forwarding event handlers and attributes
  export let className = "";
  export { className as class };
</script>

<button
  {type}
  {disabled}
  class={`btn ${variant} ${size} ${className}`}
  on:click
  {...$$restProps}
>
  <slot />
</button>

<style>
  .btn {
    border-radius: 12px;
    font-weight: 800;
    cursor: pointer;
    transition:
      transform 0.2s,
      background 0.2s,
      box-shadow 0.2s,
      opacity 0.2s;
    border: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    letter-spacing: -0.01em;
  }

  .btn.md {
    padding: 1rem 2.2rem;
    font-size: 1rem;
  }
  .btn.sm {
    padding: 0.85rem 1.3rem;
    font-size: 0.95rem;
  }

  .primary {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.28);
  }
  .primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(99, 102, 241, 0.35);
  }

  .secondary {
    background: rgba(255, 255, 255, 0.06);
    color: var(--text);
    border: 1px solid rgba(255, 255, 255, 0.12);
  }
  .secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
  }

  .ghost {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.14);
    color: var(--text);
    opacity: 0.92;
  }
  .ghost:hover {
    opacity: 1;
    transform: translateY(-1px);
  }

  .btn:disabled {
    opacity: 0.65;
    cursor: not-allowed;
    transform: none;
  }
</style>
