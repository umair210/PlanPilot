<script lang="ts">
  import Card from "$lib/components/ui/Card.svelte";
  import QuickStartForm from "$lib/components/landing/QuickStartForm.svelte";
</script>

<section class="hero">
  <div class="container">
    <div class="hero-content">
      <div class="badge">✨ Powered by AI</div>
      <h1>Turn Ambitious Goals Into Clear Action Plans</h1>
      <p>
        Stop feeling overwhelmed by big goals. PlanPilot breaks down projects
        and learning goals into a roadmap you can execute—phase by phase, task
        by task.
      </p>

      <div id="quickstart" class="quick">
        <Card padding="lg">
          <QuickStartForm />
        </Card>
      </div>
    </div>
  </div>
</section>

<style>
  .hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding: 6.2rem 0 2.5rem;
    text-align: center;
  }
  .hero-content {
    max-width: 980px;
    margin: 0 auto;
  }
  .badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.28);
    color: var(--primary);
    font-size: 0.86rem;
    margin-bottom: 1.4rem;
  }
  h1 {
    font-size: 3.6rem;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  p {
    max-width: 760px;
    margin: 0 auto 1.2rem;
    color: var(--muted);
    font-size: 1.12rem;
    line-height: 1.8;
  }
  .cta {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 1.6rem;
  }
  .quick {
    margin-top: 0.8rem;
    text-align: left;
  }

  @media (max-width: 900px) {
    h1 {
      font-size: 2.55rem;
    }
    p {
      font-size: 1.02rem;
    }
    .hero {
      padding-top: 5.2rem;
    }
  }
</style>
