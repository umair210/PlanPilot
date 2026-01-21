<section class="stats">
  <div class="container">
    <div class="grid">
      <div class="stat-card">
        <div class="stat-number">AI</div>
        <div class="stat-label">Structured plans</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">Fast</div>
        <div class="stat-label">Seconds to roadmap</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">Track</div>
        <div class="stat-label">Progress built-in</div>
      </div>
    </div>
  </div>
</section>

<style>
  .stats {
    padding: 2.8rem 0 3.6rem;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
  .stat-card {
    text-align: center;
    padding: 1.6rem;
    background: var(--panel-2);
    border-radius: var(--r-md);
    border: 1px solid rgba(255, 255, 255, 0.06);
    backdrop-filter: var(--blur);
  }
  .stat-number {
    font-size: 1.85rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .stat-label {
    color: var(--muted);
    margin-top: 0.35rem;
    font-size: 0.95rem;
  }
</style>
