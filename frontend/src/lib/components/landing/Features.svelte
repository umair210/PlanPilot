<section class="section" id="features">
  <div class="container">
    <div class="sectionHeader">
      <h2>Everything You Need to Execute</h2>
      <p>Planning is only useful when it becomes actionable.</p>
    </div>

    <div class="grid">
      <div class="feature-card">
        <div class="icon">🎯</div>
        <h3>Smart goal analysis</h3>
        <p>
          Turns a fuzzy idea into phases and concrete tasks with time estimates.
        </p>
      </div>

      <div class="feature-card">
        <div class="icon">📅</div>
        <h3>Constraint-aware</h3>
        <p>Plans adapt based on your time budget and experience level.</p>
      </div>

      <div class="feature-card">
        <div class="icon">✅</div>
        <h3>Progress tracking</h3>
        <p>Check off tasks, see progress move, and keep momentum.</p>
      </div>

      <div class="feature-card">
        <div class="icon">🧠</div>
        <h3>Clear next step</h3>
        <p>
          Each task includes acceptance criteria so you know what “done” means.
        </p>
      </div>

    </div>
  </div>
</section>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.2rem;
  }

  .feature-card {
    padding: 2rem;
    background: var(--panel-2);
    border-radius: var(--r-lg);
    border: 1px solid rgba(255, 255, 255, 0.06);
    position: relative;
    overflow: hidden;
    transition:
      transform 0.25s,
      border-color 0.25s;
  }

  .feature-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.1),
      rgba(168, 85, 247, 0.1)
    );
    opacity: 0;
    transition: opacity 0.25s;
  }

  .feature-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.25);
  }
  .feature-card:hover::before {
    opacity: 1;
  }

  .icon {
    font-size: 2.2rem;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
  }
  h3 {
    font-size: 1.35rem;
    margin-bottom: 0.7rem;
    position: relative;
    z-index: 1;
    letter-spacing: -0.02em;
  }
  p {
    color: var(--muted);
    position: relative;
    z-index: 1;
    line-height: 1.7;
  }
</style>
