<script lang="ts">
  import Button from "$lib/components/ui/Button.svelte";
  import { goto } from "$app/navigation";

  export let brand = "PlanPilot";

  function smoothScrollTo(id: string) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  }

  export let showLinks = true;
</script>

<nav class="nav">
  <div class="container navInner">
    <div class="logo" on:click={() => goto("/")}>{brand}</div>

    {#if showLinks}
      <ul class="links">
        <li>
          <a
            href="#features"
            on:click|preventDefault={() => smoothScrollTo("features")}
            >Features</a
          >
        </li>
        <li>
          <a
            href="#how-it-works"
            on:click|preventDefault={() => smoothScrollTo("how-it-works")}
            >How it works</a
          >
        </li>
      </ul>
    {/if}

    <Button
      variant="primary"
      size="sm"
      on:click={() => goto("/#quickstart")}
    >
      Get Started
    </Button>
  </div>
</nav>

<style>
  .nav {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 100;
    backdrop-filter: blur(10px);
    background: rgba(15, 23, 42, 0.7);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }
  .navInner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0;
  }
  .logo {
    font-size: 1.35rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    cursor: pointer;
  }
  .links {
    list-style: none;
    display: flex;
    gap: 26px;
  }
  .links a {
    color: var(--muted);
    text-decoration: none;
    font-size: 0.95rem;
  }
  .links a:hover {
    color: var(--text);
  }

  @media (max-width: 900px) {
    .links {
      display: none;
    }
  }
</style>
