/* ================================================================
   VSQC — shared behaviour for every page
   1. Smooth scroll (Lenis)        5. Standards search + accordion
   2. Nav + menu                   6. Contact tabs + prefill
   3. Scroll reveals + parallax    7. Forms (endpoint or email)
   4. Background video pausing     8. Portal links
   Settings come from window.VSQC_CONFIG (set in _build/content.py).
   ================================================================ */
(() => {
  'use strict';

  const CONFIG = window.VSQC_CONFIG || {};
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const VSQC = (window.VSQC = window.VSQC || {});

  /* ---------- 1. Smooth inertial scrolling (wheel only; touch stays native) ---------- */
  let lenis = null;
  if (window.Lenis && !reduceMotion) {
    lenis = new window.Lenis({ lerp: 0.085, wheelMultiplier: 0.9 });
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  VSQC.lenis = lenis;

  // Smooth in-page anchor links (#what-we-do etc.)
  document.addEventListener('click', (ev) => {
    const a = ev.target.closest('a[href^="#"]');
    if (!a || a.hasAttribute('data-scroll-step')) return;
    const id = a.getAttribute('href').slice(1);
    const target = id && document.getElementById(id);
    if (!target) return;
    ev.preventDefault();
    VSQC.closeMenu();
    const y = target.getBoundingClientRect().top + scrollY - (id === 'main' ? 0 : 80);
    if (lenis) lenis.scrollTo(y, { duration: 1.4 });
    else scrollTo({ top: y, behavior: reduceMotion ? 'auto' : 'smooth' });
  });

  /* ---------- 2. Nav: solid once scrolled; mobile menu ---------- */
  const nav = document.getElementById('nav');
  const onScrollNav = () => nav && nav.classList.toggle('is-solid', scrollY > 24);
  addEventListener('scroll', onScrollNav, { passive: true });
  onScrollNav();

  /* Glass highlight follows the pointer (decorative, mouse only) */
  document.querySelectorAll('[data-glass]').forEach((el) => {
    el.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', `${e.clientX - r.left}px`);
      el.style.setProperty('--my', `${e.clientY - r.top}px`);
      el.style.setProperty('--glow', '1');
    });
    el.addEventListener('pointerleave', () => el.style.setProperty('--glow', '0.5'));
  });

  // Lets the home page mark "Services" active while the showcase is on screen
  VSQC.setNav = (key) => {
    document.querySelectorAll('.menu__link[data-nav]').forEach((a) => {
      if (a.dataset.nav === key) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  };

  /* Menu: the pill's dropdown holds every link */
  const toggle = document.querySelector('.nav__toggle');
  const menu = document.getElementById('menu');
  const scrim = document.querySelector('.nav__scrim');
  const toggleText = document.querySelector('.nav__toggle-text');
  const isOpen = () => nav.classList.contains('is-open');

  function setMenu(open, { instant = false, restoreFocus = true } = {}) {
    if (!toggle || open === isOpen()) return;
    // Keyboard-driven close happens instantly — no animation on repeated actions
    nav.classList.toggle('no-motion', instant);
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (toggleText) toggleText.textContent = open ? 'Close' : 'Menu';
    menu.inert = !open;
    if (lenis) open ? lenis.stop() : lenis.start();
    if (open) {
      const first = menu.querySelector('[aria-current="page"]') || menu.querySelector('a');
      requestAnimationFrame(() => first && first.focus({ preventScroll: true }));
    } else if (restoreFocus && menu.contains(document.activeElement)) {
      toggle.focus({ preventScroll: true });
    }
    if (instant) requestAnimationFrame(() => requestAnimationFrame(() => nav.classList.remove('no-motion')));
  }
  VSQC.closeMenu = () => setMenu(false, { restoreFocus: false });

  if (toggle) {
    menu.inert = true;
    toggle.setAttribute('aria-label', 'Open menu');
    toggle.addEventListener('click', () => setMenu(!isOpen()));
    scrim.addEventListener('click', () => setMenu(false));
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false, { restoreFocus: false }); });
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && isOpen()) setMenu(false, { instant: true }); });
    // Tabbing out of the nav closes the menu
    nav.addEventListener('focusout', (e) => { if (isOpen() && e.relatedTarget && !nav.contains(e.relatedTarget)) setMenu(false, { restoreFocus: false }); });
  }

  /* ---------- 3. Reveal-on-scroll + hero parallax ---------- */
  const revealEls = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    // Stagger siblings that enter together
    revealEls.forEach((el) => {
      const sibs = [...el.parentElement.children].filter((c) => c.classList.contains('rv'));
      el.style.setProperty('--d', `${Math.min(sibs.indexOf(el), 6) * 70}ms`);
      io.observe(el);
    });
  } else {
    revealEls.forEach((el) => el.classList.add('in'));
  }

  const parallax = document.querySelector('[data-parallax]');
  const pheroInner = document.querySelector('.phero__inner');
  if (parallax && !reduceMotion) {
    let ticking = false;
    const update = () => {
      ticking = false;
      const h = innerHeight;
      const p = Math.min(1, Math.max(0, scrollY / h));
      // video drifts slower than the page and eases back (depth), text lifts away faster
      parallax.style.transform = `translate3d(0, ${(p * h * 0.22).toFixed(1)}px, 0) scale(${(1 - p * 0.06).toFixed(4)})`;
      if (pheroInner) {
        pheroInner.style.transform = `translate3d(0, ${(-p * h * 0.12).toFixed(1)}px, 0)`;
        pheroInner.style.opacity = String(1 - p * 1.4);
      }
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  /* ---------- 4. Pause background videos when off screen ---------- */
  const bgVideos = document.querySelectorAll('video[data-autopause]');
  if (bgVideos.length && 'IntersectionObserver' in window) {
    const vio = new IntersectionObserver((entries) => entries.forEach((en) => {
      const v = en.target;
      if (en.isIntersecting && !document.hidden) { const p = v.play(); if (p) p.catch(() => {}); }
      else v.pause();
    }));
    bgVideos.forEach((v) => vio.observe(v));
  }

  /* ---------- 5. Standards: search + accordion ---------- */
  document.querySelectorAll('[data-standards]').forEach((box) => {
    const items = [...box.querySelectorAll('.std')];
    const input = box.querySelector('[data-standards-search]');
    const count = box.querySelector('[data-standards-count]');
    const empty = box.querySelector('[data-standards-empty]');
    items.forEach((li) => {
      const btn = li.querySelector('.std__btn');
      const panel = li.querySelector('.std__panel');
      btn.addEventListener('click', () => {
        const open = btn.getAttribute('aria-expanded') !== 'true';
        btn.setAttribute('aria-expanded', String(open));
        panel.hidden = !open;
      });
    });
    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      let shown = 0;
      items.forEach((li) => {
        const hit = !q || li.dataset.search.includes(q);
        li.hidden = !hit;
        if (hit) shown++;
      });
      count.textContent = `${shown} standard${shown === 1 ? '' : 's'}`;
      empty.hidden = shown !== 0;
    });
  });

  /* ---------- 6. Contact tabs + prefill from the URL ---------- */
  const tabs = [...document.querySelectorAll('.tab[role="tab"]')];
  function selectTab(key, focus) {
    tabs.forEach((t) => {
      const on = t.dataset.tab === key;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      if (on && focus) t.focus();
    });
  }
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => selectTab(t.dataset.tab));
    t.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      selectTab(n.dataset.tab, true);
    });
  });
  if (tabs.length) {
    const qs = new URLSearchParams(location.search);
    const form = qs.get('form');
    const topic = qs.get('topic');
    const service = qs.get('service');
    if (topic && !form) selectTab('feedback');
    if (form && tabs.some((t) => t.dataset.tab === form)) selectTab(form);
    else if (!topic) selectTab('rfq');
    if (topic) document.querySelectorAll('input[name="topic"]').forEach((i) => { i.value = topic; });
    if (service) document.querySelectorAll('select[name="service"]').forEach((s) => { s.value = service; });
    if (form || topic || service) {
      // jump to the forms once the page has laid out
      addEventListener('load', () => {
        const el = document.getElementById('forms');
        if (el) scrollTo({ top: el.getBoundingClientRect().top + scrollY - 80 });
      });
    }
  }

  /* ---------- 7. Forms ---------- */
  document.querySelectorAll('[data-anonymous-form]').forEach((form) => {
    const box = form.querySelector('[data-anonymous]');
    const identity = form.querySelector('[data-identity]');
    const note = form.querySelector('[data-anon-note]');
    box.addEventListener('change', () => {
      const anon = box.checked && !!CONFIG.form_endpoint;
      identity.hidden = anon;
      identity.querySelectorAll('input').forEach((i) => { i.required = !anon; });
      note.hidden = !(box.checked && !CONFIG.form_endpoint);
    });
  });

  document.querySelectorAll('form[data-form]').forEach((form) => {
    const status = form.querySelector('.form__status');
    const btn = form.querySelector('button[type="submit"]');
    const setStatus = (msg, kind) => {
      status.textContent = msg;
      status.dataset.kind = kind || '';
    };

    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      form.classList.add('was-validated');
      if (!form.checkValidity()) {
        const bad = form.querySelector(':invalid');
        setStatus('Please complete the highlighted fields.', 'error');
        if (bad) bad.focus();
        return;
      }
      const data = new FormData(form);
      if (data.get('_gotcha')) return; // bot
      data.delete('_gotcha');
      const label = form.dataset.form;
      data.append('form', label);
      data.append('page', location.href);

      if (CONFIG.form_endpoint) {
        btn.disabled = true;
        setStatus('Sending…');
        try {
          const res = await fetch(CONFIG.form_endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
          if (!res.ok) throw new Error(res.status);
          form.reset();
          form.classList.remove('was-validated');
          setStatus('Thank you. Your message has reached VSQC — we will be in touch shortly.', 'ok');
        } catch (err) {
          setStatus(`Sorry, that didn't send. Please email ${CONFIG.email}.`, 'error');
        } finally {
          btn.disabled = false;
        }
        return;
      }

      // No form service configured: open the visitor's email app with everything filled in
      const lines = [];
      for (const [k, v] of data.entries()) {
        if (k === 'form' || k === 'page' || !String(v).trim()) continue;
        lines.push(`${k.charAt(0).toUpperCase() + k.slice(1)}: ${v}`);
      }
      const subject = `[VSQC website] ${label}${data.get('company') ? ' — ' + data.get('company') : ''}`;
      location.href = `mailto:${CONFIG.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
      setStatus('Your email app should now open with this message ready to send.', 'ok');
    });
  });

  /* ---------- 8. Portal links ---------- */
  document.querySelectorAll('[data-portal]').forEach((a) => {
    const url = CONFIG[`portal_${a.dataset.portal}_url`];
    if (url) { a.href = url; a.rel = 'noopener'; return; }
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const note = document.querySelector('[data-portal-note]');
      if (note) { note.hidden = false; note.classList.add('in'); }
    });
  });

  /* ---------- misc ---------- */
  document.querySelectorAll('[data-year]').forEach((s) => { s.textContent = new Date().getFullYear(); });
})();
