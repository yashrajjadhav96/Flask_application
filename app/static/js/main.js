document.addEventListener("DOMContentLoaded", () => {

  /* ✅ PASSWORD TOGGLE */
  const toggles = document.querySelectorAll(".toggle-password");
  toggles.forEach(toggle => {
    toggle.addEventListener("click", () => {
      const input = toggle.previousElementSibling;
      if (input.type === "password") {
        input.type = "text";
        toggle.textContent = "🙈";
      } else {
        input.type = "password";
        toggle.textContent = "👁️";
      }
    });
  });

  /* ✅ BASIC FORM VALIDATION */
  const forms = document.querySelectorAll("form");
  forms.forEach(form => {
    form.addEventListener("submit", e => {
      const inputs = form.querySelectorAll("input[required], textarea[required]");
      for (const input of inputs) {
        if (!input.value.trim()) {
          alert(`Please fill out the ${input.placeholder} field.`);
          e.preventDefault();
          return;
        }
      }
    });
  });

  document.addEventListener("input", function (e) {
    if (e.target.matches("textarea")) {
      const el = e.target;

      el.style.height = "auto";
      el.style.height = el.scrollHeight + "px";

      if (el.scrollHeight > 150) {
        el.style.height = "150px";
        el.style.overflowY = "auto";
      } else {
        el.style.overflowY = "hidden";
      }
    }
  });

});
