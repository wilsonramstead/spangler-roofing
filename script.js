/* ============================================================
   Spangler Roofing — site scripts
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

  /* ---------- Scroll reveal (IntersectionObserver, one-shot) ---------- */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    /* rootMargin bottom +12% triggers each element just before it scrolls
       into view, so it settles as it rises — matches wilsoninnovations.net */
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0, rootMargin: "0px 0px 12% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });

    /* safety net: fast momentum scrolling on phones can outrun the observer —
       anything already within the viewport gets revealed on the next scroll tick */
    var sweepTimer = null;
    var sweep = function () {
      sweepTimer = null;
      var vh = window.innerHeight;
      revealEls = revealEls.filter(function (el) {
        if (el.classList.contains("in")) return false;
        if (el.getBoundingClientRect().top < vh) {
          el.classList.add("in");
          io.unobserve(el);
          return false;
        }
        return true;
      });
    };
    window.addEventListener("scroll", function () {
      if (!sweepTimer) sweepTimer = setTimeout(sweep, 90);
    }, { passive: true });
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

  /* ---------- Estimate form -> email (mailto) ----------
     Builds a pre-filled email to Spangler Roofing in the visitor's own mail
     app. Name and phone are required. The notice explains what happened and
     gives the phone number and address as a fallback if no mail app opened.
  ------------------------------------------------------------------ */
  var estForm = document.getElementById("estimate-form");
  if (estForm) {
    var TO = "spanglerroof@gmail.com";
    estForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var val = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; };
      var name = val("name"), phone = val("phone");
      var err = document.getElementById("form-error");
      ["name", "phone"].forEach(function (id) {
        var el = document.getElementById(id);
        if (el) el.setAttribute("aria-invalid", val(id) ? "false" : "true");
      });
      if (!name || !phone) {
        if (err) { err.hidden = false; }
        (document.getElementById(!name ? "name" : "phone") || estForm).focus();
        return;
      }
      if (err) err.hidden = true;
      var lines = [
        "Name: " + name,
        "Phone: " + phone,
        "Email: " + (val("email") || "-"),
        "Property address: " + (val("address") || "-"),
        "What I need: " + (val("service") || "-"),
        "",
        "About my roof:",
        val("message") || "-",
        "",
        "(Sent from the estimate form on spanglerroofingllc.com)"
      ];
      var subject = "Free estimate request - " + name;
      var href = "mailto:" + TO + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\r\n"));
      var notice = document.getElementById("form-notice");
      if (notice) {
        notice.classList.add("show");
        notice.setAttribute("role", "status");
      }
      window.location.href = href;
      if (notice) setTimeout(function () {
        notice.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
      }, 300);
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
