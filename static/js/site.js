(() => {
  const initMenuToggles = () => {
    const menuToggle = document.getElementById("menu-toggle");
    const mobileMenu = document.getElementById("mobile-menu");
    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener("click", () => {
        mobileMenu.classList.toggle("hidden");
      });
    }

    const userMenuBtn = document.getElementById("user-menu-button");
    const userMenu = document.getElementById("user-menu");
    if (userMenuBtn && userMenu) {
      userMenuBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        userMenu.classList.toggle("hidden");
      });

      window.addEventListener("click", (e) => {
        if (!userMenuBtn.contains(e.target)) {
          userMenu.classList.add("hidden");
        }
      });
    }
  };

  const initCarousels = () => {
    const carousels = document.querySelectorAll("[data-carousel]");
    for (const carousel of carousels) {
      const viewport = carousel.querySelector("[data-carousel-viewport]");
      const track = carousel.querySelector("[data-carousel-track]");
      if (!viewport || !track) continue;

      const slides = Array.from(track.querySelectorAll("[data-carousel-slide]"));
      if (slides.length <= 1) continue;

      const prevBtn = carousel.querySelector("[data-carousel-prev]");
      const nextBtn = carousel.querySelector("[data-carousel-next]");
      const dotsWrap = carousel.querySelector("[data-carousel-dots]");

      let index = 0;
      let intervalId = null;
      let paused = false;
      const interval = Number(carousel.getAttribute("data-carousel-interval") || 5000);

      const slideLeft = (i) => {
        const slide = slides[i];
        if (!slide) return 0;
        return Math.max(0, slide.offsetLeft);
      };

      const goTo = (nextIndex) => {
        index = (nextIndex + slides.length) % slides.length;
        const left = slideLeft(index);
        viewport.scrollTo({ left, behavior: "smooth" });
        updateDots();
      };

      const buildDots = () => {
        if (!dotsWrap) return;
        dotsWrap.innerHTML = "";
        for (let i = 0; i < slides.length; i++) {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "carousel-dot";
          btn.setAttribute("aria-label", `Go to slide ${i + 1}`);
          btn.addEventListener("click", () => goTo(i));
          dotsWrap.appendChild(btn);
        }
      };

      const updateDots = () => {
        if (!dotsWrap) return;
        const dots = dotsWrap.querySelectorAll(".carousel-dot");
        dots.forEach((d, i) => {
          d.classList.toggle("carousel-dot-active", i === index);
        });
      };

      const start = () => {
        if (intervalId) return;
        intervalId = window.setInterval(() => {
          if (paused) return;
          goTo(index + 1);
        }, interval);
      };

      const stop = () => {
        if (!intervalId) return;
        window.clearInterval(intervalId);
        intervalId = null;
      };

      buildDots();
      updateDots();

      prevBtn?.addEventListener("click", () => goTo(index - 1));
      nextBtn?.addEventListener("click", () => goTo(index + 1));

      carousel.addEventListener("mouseenter", () => {
        paused = true;
      });
      carousel.addEventListener("mouseleave", () => {
        paused = false;
      });

      const ro = new ResizeObserver(() => goTo(index));
      ro.observe(viewport);

      start();

      document.addEventListener("visibilitychange", () => {
        if (document.hidden) stop();
        else start();
      });
    }
  };

  const initCountdowns = () => {
    const nodes = document.querySelectorAll("[data-countdown]");
    for (const node of nodes) {
      const dateStr = node.getAttribute("data-countdown-date");
      const timeStr = node.getAttribute("data-countdown-time") || "00:00";
      if (!dateStr) continue;

      const target = new Date(`${dateStr}T${timeStr}:00`);
      if (Number.isNaN(target.getTime())) continue;

      const daysEl = node.querySelector("[data-countdown-days]");
      const hoursEl = node.querySelector("[data-countdown-hours]");
      const minutesEl = node.querySelector("[data-countdown-minutes]");
      const secondsEl = node.querySelector("[data-countdown-seconds]");

      const pad2 = (n) => String(Math.max(0, n)).padStart(2, "0");

      const tick = () => {
        const now = new Date();
        let diff = Math.floor((target.getTime() - now.getTime()) / 1000);
        if (diff < 0) diff = 0;

        const days = Math.floor(diff / (60 * 60 * 24));
        diff -= days * 60 * 60 * 24;
        const hours = Math.floor(diff / (60 * 60));
        diff -= hours * 60 * 60;
        const minutes = Math.floor(diff / 60);
        const seconds = diff - minutes * 60;

        if (daysEl) daysEl.textContent = String(days);
        if (hoursEl) hoursEl.textContent = pad2(hours);
        if (minutesEl) minutesEl.textContent = pad2(minutes);
        if (secondsEl) secondsEl.textContent = pad2(seconds);
      };

      tick();
      window.setInterval(tick, 1000);
    }
  };

  document.addEventListener("DOMContentLoaded", () => {
    initMenuToggles();
    initCarousels();
    initCountdowns();
  });
})();
