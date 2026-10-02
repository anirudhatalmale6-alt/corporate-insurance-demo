/* Mobile nav + accessible client-side form validation. ~1 KB, no dependencies. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (ev) {
      if (ev.target.tagName === "A") {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  var form = document.querySelector(".form");
  if (!form) return;
  var status = document.getElementById("form-status");

  var rules = [
    { id: "f-name", err: "e-name", test: function (v) { return v.trim().length > 1; } },
    { id: "f-email", err: "e-email", test: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); } },
    { id: "f-msg", err: "e-msg", test: function (v) { return v.trim().length > 4; } }
  ];

  function check(rule, show) {
    var field = document.getElementById(rule.id);
    var err = document.getElementById(rule.err);
    var ok = rule.test(field.value);
    if (show) {
      err.hidden = ok;
      field.setAttribute("aria-invalid", ok ? "false" : "true");
    }
    return ok;
  }

  rules.forEach(function (rule) {
    document.getElementById(rule.id).addEventListener("blur", function () {
      check(rule, true);
    });
  });

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var first = null;
    rules.forEach(function (rule) {
      if (!check(rule, true) && !first) first = document.getElementById(rule.id);
    });
    if (first) {
      first.focus();
      status.textContent = "Please correct the highlighted fields.";
      return;
    }
    status.textContent =
      "Validated. This is the demo build, so nothing was sent — the live form delivers to your inbox.";
  });
})();
