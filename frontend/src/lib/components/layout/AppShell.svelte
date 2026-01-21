<script lang="ts">
  import Background from "$lib/components/layout/Background.svelte";
  import TopNav from "$lib/components/layout/TopNav.svelte";
  export let title: string | null = null;
</script>

<Background />
<TopNav brand="PlanPilot" showLinks={false} />

<main class="shell">
  <div class="container">
    {#if title}
      <h1 class="pageTitle">{title}</h1>
    {/if}
    <slot />
  </div>
</main>

<style>
  .shell {
    padding-top: 92px;
    padding-bottom: 60px;
  }
  .pageTitle {
    font-size: 2rem;
    letter-spacing: -0.03em;
    margin-bottom: 14px;
  }
</style>
