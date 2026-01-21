<div class="bg-gradient"></div>
<div class="bg-orbs" aria-hidden="true">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
</div>

<style>
  .bg-gradient {
    position: fixed;
    inset: 0;
    background: linear-gradient(
      135deg,
      var(--bg-darker) 0%,
      var(--bg-dark) 50%,
      #1e1b4b 100%
    );
    z-index: -2;
  }

  .bg-orbs {
    position: fixed;
    inset: 0;
    z-index: -1;
    overflow: hidden;
  }

  .orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.15;
    animation: float 20s infinite ease-in-out;
  }

  .orb1 {
    width: 600px;
    height: 600px;
    background: var(--primary);
    top: -300px;
    left: -200px;
  }
  .orb2 {
    width: 500px;
    height: 500px;
    background: var(--secondary);
    bottom: -250px;
    right: -150px;
    animation-delay: -5s;
  }
  .orb3 {
    width: 400px;
    height: 400px;
    background: var(--accent);
    top: 50%;
    left: 50%;
    animation-delay: -10s;
  }

  @keyframes float {
    0%,
    100% {
      transform: translate(0, 0) rotate(0deg);
    }
    33% {
      transform: translate(50px, -50px) rotate(120deg);
    }
    66% {
      transform: translate(-30px, 30px) rotate(240deg);
    }
  }
</style>
