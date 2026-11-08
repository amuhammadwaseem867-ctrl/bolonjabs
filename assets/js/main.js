/* N Maphikana Plumbing: interactions & animations
   - Works without GSAP (content is visible by default; .js-anim only hides reveal targets).
   - Respects prefers-reduced-motion. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGSAP = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  var root = document.documentElement;

  // If animations are expected but GSAP failed to load, reveal everything.
  if (!hasGSAP) root.classList.remove('js-anim');

  /* ---------- Year ---------- */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  /* ---------- Preloader: live plumbing system ----------
     Water flows through the pipes, the valve turns and the pressure gauge
     climbs as the page loads; at 100% the tap pours and the screen floods. */
  var heroPlay = null;   // set by the GSAP section
  var preGone = false;
  (function preloader() {
    var pre = document.getElementById('preloader');
    if (!pre) { preGone = true; root.classList.remove('is-loading'); return; }
    var water = document.getElementById('plWaterPath');
    var maskPath = document.getElementById('plMaskPath');
    var wheel = document.getElementById('plWheel');
    var needle = document.getElementById('plNeedle');
    var arc = document.getElementById('plArcVal');
    var pct = document.getElementById('plPct');
    var msg = document.getElementById('plMsg');
    var stream = document.getElementById('plStream');
    var flood = document.getElementById('plFlood');
    var messages = [[0, 'Checking the pipes…'], [30, 'Opening the valve…'], [60, 'Building pressure…'], [92, "Water's flowing!"]];
    var shown = 0, target = 6, loaded = false, finished = false, lastMsg = '';
    var start = performance.now();
    var minTime = reduceMotion ? 300 : 2200;

    var tracked = [].slice.call(document.querySelectorAll('img:not([loading="lazy"])'));
    var total = tracked.length + 1, done = 0;
    function bump() { done++; target = Math.max(target, Math.min(90, 6 + (done / total) * 84)); }
    tracked.forEach(function (img) {
      if (img.complete) bump();
      else { img.addEventListener('load', bump, { once: true }); img.addEventListener('error', bump, { once: true }); }
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(bump); else bump();
    function allLoaded() { loaded = true; target = 100; }
    if (document.readyState === 'complete') allLoaded(); else window.addEventListener('load', allLoaded);
    setTimeout(allLoaded, 6500); // never wait longer than this

    function render() {
      var off = (100 - shown).toFixed(2);
      water.setAttribute('stroke-dashoffset', off);
      maskPath.setAttribute('stroke-dashoffset', off);
      arc.setAttribute('stroke-dashoffset', off);
      wheel.setAttribute('transform', 'rotate(' + (shown * 7.2).toFixed(1) + ' 290 138)');
      needle.setAttribute('transform', 'rotate(' + (-130 + shown * 2.6).toFixed(1) + ' 360 84)');
      pct.textContent = Math.round(shown) + '%';
      var m = messages[0][1];
      messages.forEach(function (x) { if (shown >= x[0]) m = x[1]; });
      if (m !== lastMsg) { msg.textContent = m; lastMsg = m; }
    }
    function tick(now) {
      // water only starts once the pipes have drawn in
      var cap = now - start < 900 ? 0 : target;
      shown += Math.max(0, (cap - shown) * 0.05 + (cap > shown ? 0.2 : 0));
      if (shown > cap) shown = cap;
      render();
      if (shown >= 100 && loaded && now - start > minTime) return exit();
      requestAnimationFrame(tick);
    }
    function cleanup() {
      if (pre.parentNode) pre.parentNode.removeChild(pre);
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
    }
    function exit() {
      if (finished) return; finished = true;
      preGone = true;
      if (hasGSAP && !reduceMotion) {
        var g = window.gsap;
        pre.classList.add('is-pouring');
        g.timeline({
          onComplete: cleanup
        })
          .to(stream, { attr: { transform: 'scale(1 1)' }, duration: 0.35, ease: 'power2.in' })
          .to(needle, { attr: { transform: 'rotate(140 360 84)' }, duration: 0.25, ease: 'power1.out', yoyo: true, repeat: 1 }, 0)
          .to(flood, { yPercent: -102, duration: 0.9, ease: 'power2.inOut' }, 0.25)
          .add(function () {
            pre.classList.add('is-done');
            root.classList.remove('is-loading');
            g.set('.preloader__inner', { autoAlpha: 0 });
          }, 1.1)
          .to(pre, { yPercent: -120, duration: 1, ease: 'power4.inOut' }, 1.15)
          .add(function () { if (heroPlay) heroPlay(); }, 1.45);
      } else {
        pre.classList.add('is-done');
        root.classList.remove('is-loading');
        pre.style.transition = 'opacity .35s ease';
        pre.style.opacity = '0';
        setTimeout(cleanup, 380);
      }
    }
    if (reduceMotion) { shown = 0; }
    requestAnimationFrame(tick);
  })();

  /* ---------- Header state + progress bar ---------- */
  var header = document.getElementById('header');
  var bar = document.getElementById('progressBar');
  var ticking = false;
  function onScroll() {
    var st = window.scrollY;
    header.classList.toggle('is-scrolled', st > 40);
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (h > 0 ? st / h : 0) + ')';
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Mobile drawer ---------- */
  var drawer = document.getElementById('drawer');
  var openBtn = document.getElementById('menuOpen');
  var closeBtn = document.getElementById('menuClose');
  function setDrawer(open) {
    drawer.classList.toggle('is-open', open);
    openBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) closeBtn.focus(); else openBtn.focus();
  }
  openBtn.addEventListener('click', function () { setDrawer(true); });
  closeBtn.addEventListener('click', function () { setDrawer(false); });
  drawer.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      drawer.classList.remove('is-open');
      openBtn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer.classList.contains('is-open')) setDrawer(false);
  });

  /* ---------- Reviews pause toggle ---------- */
  var rBox = document.getElementById('reviewsBox');
  var rBtn = document.getElementById('reviewsPause');
  if (rBox && rBtn) {
    if (reduceMotion) rBtn.hidden = true;
    rBtn.addEventListener('click', function () {
      var paused = rBox.classList.toggle('is-paused');
      rBtn.setAttribute('aria-pressed', String(paused));
      rBtn.querySelector('span').textContent = paused ? 'Play reviews' : 'Pause reviews';
    });
  }

  /* ---------- Quote form ---------- */
  var form = document.getElementById('quoteForm');
  if (form) {
    var status = document.getElementById('formStatus');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.elements.name, phone = form.elements.phone;
      var phoneOk = phone.value.replace(/[^\d+]/g, '').length >= 9;
      var nameOk = name.value.trim().length > 1;
      name.setAttribute('aria-invalid', String(!nameOk));
      phone.setAttribute('aria-invalid', String(!phoneOk));
      status.className = 'form__status';
      if (!nameOk || !phoneOk) {
        status.textContent = '';
        (!nameOk ? name : phone).focus();
        return;
      }
      // Front-end only: connect to a form service (e.g. Formspree, Netlify Forms) to receive leads.
      status.classList.add('ok');
      status.textContent = 'Thank you! A plumber from N Maphikana Plumbing will call you shortly.';
      form.reset();
    });
    ['name', 'phone'].forEach(function (id) {
      form.elements[id].addEventListener('input', function () { this.removeAttribute('aria-invalid'); });
    });
  }

  if (!hasGSAP || reduceMotion) return;

  /* =================== GSAP animations =================== */
  var gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger);
  var ease = 'power3.out';

  // Hero intro
  var tl = gsap.timeline({ paused: true, defaults: { ease: ease } });
  tl.fromTo('#heroImg', { scale: 1.22 }, { scale: 1.08, duration: 2.2, ease: 'power2.out' }, 0)
    .from('[data-hero-line]', { yPercent: 110, duration: 1.1, stagger: 0.12 }, 0.2)
    .from('[data-hero]', { y: 30, opacity: 0, duration: 0.9, stagger: 0.1 }, 0.45)
    .from('.header', { y: -30, opacity: 0, duration: 0.8 }, 0.3);
  // Play once the preloader has lifted (or immediately if it already has)
  heroPlay = function () { tl.play(); };
  if (preGone) tl.play();

  // Hero parallax on scroll
  gsap.to('#heroImg', {
    yPercent: 12, ease: 'none',
    scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
  });

  // Generic reveals (batched for smooth staggers)
  window.ScrollTrigger.batch('[data-reveal]', {
    start: 'top 88%',
    once: true,
    onEnter: function (els) {
      gsap.to(els, {
        opacity: 1, y: 0, duration: 1, ease: ease, stagger: 0.09, overwrite: true,
        onComplete: function () {
          els.forEach(function (el) { el.classList.add('is-in'); });
          gsap.set(els, { clearProps: 'transform,opacity' }); // hand hover effects back to CSS
        }
      });
    }
  });

  // Image parallax inside frames
  gsap.utils.toArray('[data-parallax]').forEach(function (img) {
    gsap.fromTo(img, { yPercent: -8 }, {
      yPercent: 0, ease: 'none',
      scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true }
    });
  });

  // Gallery tiles: clip reveal
  gsap.utils.toArray('.tile img').forEach(function (img) {
    gsap.from(img, {
      scale: 1.25, duration: 1.6, ease: 'power2.out',
      scrollTrigger: { trigger: img, start: 'top 90%', once: true }
    });
  });

  // Counters
  gsap.utils.toArray('[data-count]').forEach(function (el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    var obj = { v: 0 };
    el.textContent = (0).toFixed(decimals);
    gsap.to(obj, {
      v: target, duration: 2, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      onUpdate: function () {
        el.textContent = decimals ? obj.v.toFixed(decimals) : String(Math.round(obj.v)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      }
    });
  });

  // Process line draws as you scroll
  gsap.fromTo('#processLine', { scaleX: 0 }, {
    scaleX: 1, ease: 'none',
    scrollTrigger: { trigger: '.process', start: 'top 75%', end: 'bottom 55%', scrub: 0.6 }
  });

  // Refresh after images load to keep trigger positions accurate
  window.addEventListener('load', function () { window.ScrollTrigger.refresh(); });
})();
