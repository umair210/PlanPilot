<script lang="ts">
  import { onMount } from "svelte";
  import Background from "$lib/components/layout/Background.svelte";
  import TopNav from "$lib/components/layout/TopNav.svelte";

  import Hero from "$lib/components/landing/Hero.svelte";
  import Stats from "$lib/components/landing/Stats.svelte";
  import Features from "$lib/components/landing/Features.svelte";
  import HowItWorks from "$lib/components/landing/HowItWorks.svelte";
  import FinalCta from "$lib/components/landing/FinalCta.svelte";
  import Footer from "$lib/components/landing/Footer.svelte";

  import {
    animateIn,
    staggerOnScroll,
    revealSteps,
  } from "$lib/animations/gsap";

  onMount(() => {
    animateIn(".hero-content", { y: 40, duration: 0.95, delay: 0.15 });
    staggerOnScroll(".stat-card", ".stats", { y: 26, stagger: 0.1 });
    staggerOnScroll(".feature-card", "#features", {
      y: 40,
      stagger: 0.12,
      start: "top 70%",
    });
    revealSteps(".step");
    staggerOnScroll(".cta-box", ".final-cta", {
      y: 20,
      stagger: 0.1,
      start: "top 75%",
    });
  });
</script>

<Background />
<TopNav brand="PlanPilot" showLinks={true} />

<main class="page">
  <Hero />
  <Stats />
  <Features />
  <HowItWorks />
  <FinalCta />
  <Footer />
</main>

<style>
  .page {
    padding-top: 76px;
  } /* space for fixed nav */
</style>
