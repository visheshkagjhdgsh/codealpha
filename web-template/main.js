const THEME_STORAGE_KEY = "webtemplate.theme";

function getSystemPrefersDark() {
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function getInitialTheme() {
  const stored = localStorage.getItem(THEME_STORAGE_KEY);
  if (stored === "light" || stored === "dark") return stored;
  return getSystemPrefersDark() ? "dark" : "light";
}

function applyTheme(theme) {
  const root = document.documentElement;
  if (theme === "dark") {
    root.removeAttribute("data-theme");
  } else {
    root.setAttribute("data-theme", "light");
  }
  localStorage.setItem(THEME_STORAGE_KEY, theme);
}

function toggleTheme() {
  const isDark = !document.documentElement.hasAttribute("data-theme");
  applyTheme(isDark ? "light" : "dark");
  updateThemeToggleIcon();
}

function updateThemeToggleIcon() {
  const isDark = !document.documentElement.hasAttribute("data-theme");
  const toggle = document.querySelector("#theme-toggle");
  if (!toggle) return;
  toggle.textContent = isDark ? "🌙" : "☀️";
  toggle.setAttribute("aria-label", `Switch to ${isDark ? "light" : "dark"} theme`);
}

// Set current year
(function setYear() {
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();

// Init theme early to avoid FOUC
applyTheme(getInitialTheme());
updateThemeToggleIcon();

// Wire up events
window.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("theme-toggle");
  if (toggle) toggle.addEventListener("click", toggleTheme);

  const cta = document.getElementById("cta");
  if (cta) cta.addEventListener("click", (e) => {
    // In a real app, you might navigate; we just give feedback
    const btn = e.currentTarget;
    btn.classList.add("success");
    btn.textContent = "Copied to your project!";
    setTimeout(() => {
      btn.classList.remove("success");
      btn.textContent = "Use this template";
    }, 1400);
  });
});