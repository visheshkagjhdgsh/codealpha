document.addEventListener("DOMContentLoaded", () => {
  const html = document.documentElement;
  const navToggle = document.querySelector(".nav-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  const themeToggle = document.querySelector(".theme-toggle");
  const contactForm = document.getElementById("contact-form");
  const statusEl = document.querySelector(".form-status");
  const yearEl = document.getElementById("year");

  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  if (navToggle && mobileMenu) {
    navToggle.addEventListener("click", () => {
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
      mobileMenu.hidden = expanded;
      mobileMenu.style.display = expanded ? "none" : "block";
    });

    mobileMenu.addEventListener("click", (e) => {
      const target = e.target;
      if (target instanceof HTMLElement && target.tagName === "A") {
        mobileMenu.hidden = true;
        navToggle.setAttribute("aria-expanded", "false");
        mobileMenu.style.display = "none";
      }
    });
  }

  if (themeToggle) {
    const preferred = localStorage.getItem("theme");
    if (preferred === "light") html.classList.add("light");

    themeToggle.addEventListener("click", () => {
      html.classList.toggle("light");
      const isLight = html.classList.contains("light");
      localStorage.setItem("theme", isLight ? "light" : "");
    });
  }

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (e) => {
      const href = anchor.getAttribute("href");
      if (!href) return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  function setError(id, message) {
    const error = document.querySelector(`.error[data-for="${id}"]`);
    if (error) error.textContent = message || "";
  }

  function validate(formData) {
    let ok = true;
    const name = String(formData.get("name") || "").trim();
    const email = String(formData.get("email") || "").trim();
    const message = String(formData.get("message") || "").trim();

    setError("name", "");
    setError("email", "");
    setError("message", "");

    if (!name) { setError("name", "Please enter your name"); ok = false; }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { setError("email", "Enter a valid email"); ok = false; }
    if (!message) { setError("message", "Please enter a message"); ok = false; }

    return ok;
  }

  if (contactForm) {
    contactForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!statusEl) return;
      const formData = new FormData(contactForm);
      if (!validate(formData)) return;
      statusEl.textContent = "Sending...";

      try {
        await new Promise((r) => setTimeout(r, 700));
        statusEl.textContent = "Thanks! We'll be in touch soon.";
        contactForm.reset();
      } catch (err) {
        statusEl.textContent = "Something went wrong. Please try again.";
      }
    });
  }
});