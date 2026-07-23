/* ============================================================
   Spangler Roofing — demo site scripts
   Vanilla JS, no dependencies. Runs from file://.
   ============================================================ */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Sticky header shadow ---------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Mobile nav drawer ---------- */
  var navToggle = document.querySelector(".nav-toggle");
  var mobileNav = document.querySelector(".mobile-nav");
  if (navToggle && mobileNav) {
    var closeEls = mobileNav.querySelectorAll("[data-close-nav]");
    var openNav = function () {
      mobileNav.classList.add("open");
      document.body.style.overflow = "hidden";
      navToggle.setAttribute("aria-expanded", "true");
    };
    var closeNav = function () {
      mobileNav.classList.remove("open");
      document.body.style.overflow = "";
      navToggle.setAttribute("aria-expanded", "false");
    };
    navToggle.addEventListener("click", openNav);
    mobileNav.addEventListener("click", function (e) {
      if (e.target === mobileNav) closeNav();
    });
    closeEls.forEach(function (el) { el.addEventListener("click", closeNav); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && mobileNav.classList.contains("open")) closeNav();
    });
  }

  /* ---------- Scroll reveal (IntersectionObserver) ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- FAQ accordion ---------- */
  var faqs = document.querySelectorAll(".faq");
  faqs.forEach(function (faq) {
    var q = faq.querySelector(".faq-q");
    var a = faq.querySelector(".faq-a");
    if (!q || !a) return;
    q.addEventListener("click", function () {
      var isOpen = faq.classList.contains("open");
      // close others
      faqs.forEach(function (other) {
        if (other !== faq) {
          other.classList.remove("open");
          var oa = other.querySelector(".faq-a");
          var oq = other.querySelector(".faq-q");
          if (oa) oa.style.maxHeight = null;
          if (oq) oq.setAttribute("aria-expanded", "false");
        }
      });
      if (isOpen) {
        faq.classList.remove("open");
        a.style.maxHeight = null;
        q.setAttribute("aria-expanded", "false");
      } else {
        faq.classList.add("open");
        a.style.maxHeight = a.scrollHeight + "px";
        q.setAttribute("aria-expanded", "true");
      }
    });
  });

  /* ---------- Estimate form (DEMO ONLY) ----------
     Demo mode: we do NOT submit anywhere. We show a friendly inline
     notice and surface the phone number.
     TO GO LIVE: wire this form to a form service (e.g. Formspree,
     Netlify Forms, or a backend endpoint) — set the <form> action/method
     or POST the FormData below, then remove the preventDefault demo block.
  ------------------------------------------------------------------ */
  var estForm = document.getElementById("estimate-form");
  if (estForm) {
    estForm.addEventListener("submit", function (e) {
      e.preventDefault();
      // var data = new FormData(estForm); // <-- send this to your form service on launch
      var notice = document.getElementById("form-notice");
      if (notice) {
        notice.classList.add("show");
        notice.setAttribute("role", "status");
        notice.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
      }
      estForm.querySelectorAll("input,textarea,select,button").forEach(function (el) {
        if (el.type !== "button") el.setAttribute("aria-disabled", "true");
      });
    });
  }

  /* ---------- Gallery lightbox ---------- */
  var lightbox = document.getElementById("lightbox");
  if (lightbox) {
    var lbImg = lightbox.querySelector("img");
    var items = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]"));
    var current = 0;

    var show = function (i) {
      current = (i + items.length) % items.length;
      var src = items[current].getAttribute("data-full") ||
                (items[current].querySelector("img") && items[current].querySelector("img").src);
      var alt = items[current].querySelector("img") ? items[current].querySelector("img").alt : "";
      if (src) { lbImg.src = src; lbImg.alt = alt; }
    };
    var open = function (i) {
      show(i);
      lightbox.classList.add("open");
      document.body.style.overflow = "hidden";
    };
    var close = function () {
      lightbox.classList.remove("open");
      document.body.style.overflow = "";
      lbImg.src = "";
    };

    items.forEach(function (item, i) {
      item.addEventListener("click", function () { open(i); });
      item.setAttribute("tabindex", "0");
      item.setAttribute("role", "button");
      item.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(i); }
      });
    });

    lightbox.querySelector(".lightbox-close").addEventListener("click", close);
    lightbox.querySelector(".lightbox-nav.prev").addEventListener("click", function () { show(current - 1); });
    lightbox.querySelector(".lightbox-nav.next").addEventListener("click", function () { show(current + 1); });
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lightbox.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
  }

  /* ---------- Footer year ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
