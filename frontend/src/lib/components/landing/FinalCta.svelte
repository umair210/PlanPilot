<script lang="ts">
  import Card from "$lib/components/ui/Card.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import { goto } from "$app/navigation";
</script>

<section class="final-cta">
  <div class="container">
    <div class="cta-box">
      <Card padding="lg">
        <div class="inner">
          <h2>Ready to turn ambition into execution?</h2>
          <p class="muted">Create a plan and start completing tasks today.</p>
          <div class="actions">
            <Button variant="primary" on:click={() => goto("/#quickstart")}
              >Create a plan</Button
            >
          </div>
        </div>
      </Card>
    </div>
  </div>
</section>

<style>
  .final-cta {
    padding: 6.5rem 0 5.5rem;
    text-align: center;
  }
  .cta-box {
    max-width: 860px;
    margin: 0 auto;
  }
  .inner {
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: center;
  }
  h2 {
    font-size: 2.35rem;
    letter-spacing: -0.03em;
  }
  p {
    font-size: 1.05rem;
  }
  .actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 6px;
  }
</style>
