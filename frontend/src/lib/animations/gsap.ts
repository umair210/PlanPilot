import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

let registered = false;

export function ensureGsap() {
  if (!registered) {
    gsap.registerPlugin(ScrollTrigger);
    registered = true;
  }
  return { gsap, ScrollTrigger };
}

/**
 * Fade + move up on mount
 */
export function animateIn(selector: string, opts?: { delay?: number; y?: number; duration?: number }) {
  const { gsap } = ensureGsap();
  gsap.from(selector, {
    opacity: 0,
    y: opts?.y ?? 30,
    duration: opts?.duration ?? 0.8,
    delay: opts?.delay ?? 0,
    ease: "power2.out"
  });
}

/**
 * Stagger in on scroll
 */
export function staggerOnScroll(
  selector: string,
  trigger: string,
  opts?: { start?: string; y?: number; duration?: number; stagger?: number }
) {
  const { gsap } = ensureGsap();
  gsap.from(selector, {
    scrollTrigger: {
      trigger,
      start: opts?.start ?? "top 75%"
    },
    opacity: 0,
    y: opts?.y ?? 30,
    duration: opts?.duration ?? 0.7,
    stagger: opts?.stagger ?? 0.12,
    ease: "power2.out"
  });
}

/**
 * Reveal steps one by one on scroll (good for "how it works")
 */
export function revealSteps(selector: string) {
  const { gsap } = ensureGsap();
  document.querySelectorAll<HTMLElement>(selector).forEach((el, idx) => {
    gsap.to(el, {
      scrollTrigger: {
        trigger: el,
        start: "top 85%"
      },
      opacity: 1,
      x: 0,
      duration: 0.75,
      delay: idx * 0.12,
      ease: "power2.out"
    });
  });
}
