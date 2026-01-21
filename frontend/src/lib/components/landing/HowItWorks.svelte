<section class="how section" id="how-it-works">
  <div class="container">
    <div class="sectionHeader">
      <h2>From Goal to Action in 3 Steps</h2>
      <p>A simple loop: generate → execute → track.</p>
    </div>

    <div class="steps">
      <div class="step">
        <div class="num">1</div>
        <div class="content">
          <h3>Describe your goal</h3>
          <p>Add context like experience level and time budget.</p>
        </div>
      </div>

      <div class="step">
        <div class="num">2</div>
        <div class="content">
          <h3>AI builds your roadmap</h3>
          <p>
            Get phases + tasks with estimates and clear acceptance criteria.
          </p>
        </div>
      </div>

      <div class="step">
        <div class="num">3</div>
        <div class="content">
          <h3>Execute & track</h3>
          <p>Mark tasks done, adjust as you go, and keep momentum.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .how {
    background: rgba(255, 255, 255, 0.02);
  }

  .steps {
    max-width: 1000px;
    margin: 0 auto;
  }

  .step {
    display: grid;
    grid-template-columns: 76px 1fr;
    gap: 1.5rem;
    margin-bottom: 2.4rem;
    opacity: 0;
    transform: translateX(-50px);
  }

  .num {
    width: 76px;
    height: 76px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 900;
  }

  .content h3 {
    font-size: 1.7rem;
    margin-bottom: 0.6rem;
    letter-spacing: -0.02em;
  }
  .content p {
    color: var(--muted);
    font-size: 1.05rem;
    line-height: 1.75;
  }

  @media (max-width: 900px) {
    .step {
      grid-template-columns: 1fr;
    }
    .num {
      width: 60px;
      height: 60px;
      font-size: 1.5rem;
    }
  }
</style>
