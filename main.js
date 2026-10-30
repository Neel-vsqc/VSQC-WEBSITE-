/* ================================================================
   VSQC — hero + scroll-driven services showcase
   ----------------------------------------------------------------
   1. CONFIG            tweak timings here
   2. VideoStage        swaps 4 stacked <video> layers, never blank
   3. Scroll controller maps scroll position → step (-1 = hero, 0–6)
   4. Text              word-split titles, enter / leave classes
   5. Camera            subtle 3D dolly + pointer tilt on the video
   6. Nav, menu, smooth scroll, visibility
   ================================================================ */
(() => {
  'use strict';

  /* ---------------------------------------------------------------
     1. CONFIG
     Clip map:  clip-1 hero loop
                clip-2 hero → service 1 transition
                clip-3 service 1 loop, clip-4 1 → 2, clip-5 service 2 loop …
                clip-15 service 7 loop
     --------------------------------------------------------------- */
  const CONFIG = {
    transitionRate: 2.6,  // transition clips are 10 s slow morphs → ~3.8 s on screen
    catchUpRate: 5,       // if the user scrolls on mid-transition, finish it quickly
    textDelay: 0.3,       // s after a transition starts that the new text slides in
    startBlend: 0.3,      // tiny blend from a mid-loop frame into a transition's first frame
    crossfade: 0.7,       // backward / multi-step jumps (spec: 0.6–0.8 s)
    textFallback: 6000,   // show text anyway if a video never loads
  };

  const clipSrc = (n) => `clip-${n}.mp4`;
  const loopClipFor = (step) => (step < 0 ? 1 : 3 + step * 2);
  const transitionClipFor = (step) => 2 + step * 2; // transition INTO `step`

  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');

  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const once = (el, ev) => new Promise((r) => el.addEventListener(ev, r, { once: true }));
  const play = (v) => { const p = v.play(); if (p) p.catch(() => {}); };

  /* ---------------------------------------------------------------
     2. VideoStage
     - Each layer is a <video>. The visible one is `front`.
     - New content is always placed ON TOP of what is showing, and
       only once it has a decoded frame, so nothing blank ever shows.
     - Forward 1 step:   transition clip → instant cut to loop clip
     - Anything else:    crossfade straight to the target loop clip
     --------------------------------------------------------------- */
  class VideoStage {
    constructor(videos, onArrive) {
      this.layers = videos.map((el) => ({ el, clip: 0, used: 0 }));
      this.onArrive = onArrive;   // called when a step's visual has "landed"
      this.front = null;          // visible layer
      this.pending = null;        // layer being prepared for display
      this.current = null;        // step whose visual is showing / settling
      this.transition = null;     // { step, layer, queued, cued } while one plays
      this.token = 0;             // bumps on every new operation; stale ops bail
      this.z = 1;
      this.active = true;         // false when the section is off screen
    }

    /* Find the layer holding `clip`, or load it into the least-recently
       used layer that is not on screen or in use. */
    layerFor(clip, keep = []) {
      let layer = this.layers.find((l) => l.clip === clip);
      if (layer) return layer;
      const busy = new Set([this.front, this.pending, this.transition && this.transition.layer, ...keep]);
      const free = this.layers.filter((l) => !busy.has(l)).sort((a, b) => a.used - b.used);
      // Prefer layers that are already hidden; never blank one that is still on screen if avoidable
      layer = free.find((l) => !l.el.classList.contains('is-visible')) || free[0];
      if (!layer) return this.front; // should never happen with 4 layers
      layer.clip = clip;
      layer.used = performance.now();
      layer.el.src = clipSrc(clip);
      layer.el.preload = 'auto';
      layer.el.load();
      return layer;
    }

    /* Resolve once the layer has a frame to show (optionally at time 0). */
    async ready(layer, rewind) {
      const v = layer.el;
      if (v.readyState < 2) await Promise.race([once(v, 'loadeddata'), wait(8000)]);
      if (rewind && v.currentTime > 0.01) {
        v.currentTime = 0;
        await Promise.race([once(v, 'seeked'), wait(1500)]);
      }
    }

    /* Put `layer` on top. fade = 0 → instant cut. Others are hidden after. */
    reveal(layer, fade) {
      const v = layer.el;
      layer.used = performance.now();
      v.style.zIndex = ++this.z;
      v.style.transition = fade ? `opacity ${fade}s cubic-bezier(.45,0,.25,1)` : 'none';
      v.classList.add('is-visible');
      this.front = layer;
      if (this.pending === layer) this.pending = null;
      const hideOthers = () => {
        if (this.front !== layer) return;
        this.layers.forEach((l) => {
          if (l === layer || l === this.pending) return;
          l.el.style.transition = 'none';
          l.el.classList.remove('is-visible');
          l.el.pause();
        });
      };
      if (fade) setTimeout(hideOthers, fade * 1000 + 60);
      else requestAnimationFrame(() => requestAnimationFrame(hideOthers));
    }

    /* Public: go to a step (-1 = hero). */
    goTo(step) {
      const t = this.transition;
      if (t) {
        if (step === t.step) {                 // user came back to the step being entered
          t.queued = null;
          t.layer.el.playbackRate = CONFIG.transitionRate;
          return;
        }
        if (step === t.step + 1 && !reduceMotion.matches) {
          t.queued = step;                     // finish this one fast, then chain the next
          t.layer.el.playbackRate = CONFIG.catchUpRate;
          return;
        }
        this.transition = null;                // backward / far jump: cancel, crossfade
        this.crossfadeTo(step);
        return;
      }
      if (step === this.current) return;
      if (!reduceMotion.matches && this.current !== null && step === this.current + 1) {
        this.playTransition(step, false);
      } else {
        this.crossfadeTo(step, this.current === null ? 0.5 : CONFIG.crossfade);
      }
    }

    /* Forward one step: transition clip, then a frame-perfect cut to the loop. */
    async playTransition(step, chained) {
      const token = ++this.token;
      const layer = this.layerFor(transitionClipFor(step));
      const t = (this.transition = { step, layer, queued: null, cued: false });
      const v = layer.el;
      v.loop = false;
      this.pending = layer;
      await this.ready(layer, true);
      if (this.transition !== t || token !== this.token) return;

      v.playbackRate = CONFIG.transitionRate;

      // A loop clip only matches the transition's first frame at its own start/end.
      // Mid-loop, blend for a fraction of a second so the hand-off stays invisible.
      let blend = 0;
      const out = this.front && this.front.el;
      if (!chained && out && out.duration) {
        const pos = out.currentTime % out.duration;
        if (pos > 0.2 && out.duration - pos > 0.2) blend = CONFIG.startBlend;
      }
      this.reveal(layer, blend);
      if (this.active) play(v);

      // Preload the loop we will cut to
      this.layerFor(loopClipFor(step), [layer]);

      // Text slides in alongside the video instead of waiting for it to finish
      setTimeout(() => {
        if (this.transition === t && !t.cued && t.queued === null) { t.cued = true; this.onArrive(step); }
      }, CONFIG.textDelay * 1000);

      const onEnded = () => {
        if (this.transition !== t) return;
        this.transition = null;
        this.current = step;
        if (t.queued !== null) { this.playTransition(t.queued, true); return; }
        if (!t.cued) this.onArrive(step);
        this.cutToLoop(step);
      };
      v.addEventListener('ended', onEnded, { once: true });
    }

    /* Transition finished: its last frame == the loop's first frame → hard cut. */
    async cutToLoop(step) {
      const token = ++this.token;
      const layer = this.layerFor(loopClipFor(step));
      layer.el.loop = true;
      layer.el.playbackRate = 1;
      this.pending = layer;
      await this.ready(layer, true);   // while waiting, the transition's last frame stays up
      if (token !== this.token) return;
      this.reveal(layer, 0);
      if (this.active) play(layer.el);
      setTimeout(() => token === this.token && this.preloadAround(step), 300);
    }

    /* Backward / jump / reduced motion: soft crossfade to the target loop. */
    async crossfadeTo(step, fade = CONFIG.crossfade) {
      const token = ++this.token;
      this.current = step;
      const layer = this.layerFor(loopClipFor(step));
      if (layer === this.front) {
        if (this.active) play(layer.el);
        this.onArrive(step);
        return;
      }
      layer.el.loop = true;
      layer.el.playbackRate = 1;
      this.pending = layer;
      await this.ready(layer, false);
      if (token !== this.token) return;
      this.reveal(layer, fade);
      if (this.active) play(layer.el);
      setTimeout(() => token === this.token && this.onArrive(step), fade * 450);
      setTimeout(() => token === this.token && this.preloadAround(step), fade * 1000 + 200);
    }

    /* Keep the likely next clips loaded in the spare layers. */
    preloadAround(step) {
      const keep = [];
      const want = [];
      if (step + 1 <= 6) want.push(transitionClipFor(step + 1), loopClipFor(step + 1));
      if (step >= 0) want.push(loopClipFor(step - 1));
      want.forEach((clip) => keep.push(this.layerFor(clip, keep)));
    }

    /* Pause everything when the section is off screen. */
    setActive(on) {
      if (on === this.active) return;
      this.active = on;
      const v = this.front && this.front.el;
      if (!v) return;
      if (on && !v.ended) play(v);
      else v.pause();
    }
  }

  /* ---------------------------------------------------------------
     DOM
     --------------------------------------------------------------- */
  const nav = document.getElementById('nav');
  const showcase = document.querySelector('.showcase');
  const stageEl = document.getElementById('stage');
  const camera = document.getElementById('camera');
  const hero = document.getElementById('hero');
  const ui = document.getElementById('services-ui');
  const articles = [...document.querySelectorAll('.svc')];
  const STEPS = articles.length;

  /* ---------------------------------------------------------------
     4. Text — split titles into masked words
     --------------------------------------------------------------- */
  articles.forEach((a) => {
    const h = a.querySelector('.svc__title');
    const words = h.textContent.trim().split(/\s+/);
    h.setAttribute('aria-label', h.textContent.trim());
    h.innerHTML = words
      .map((w, i) => `<span class="w" aria-hidden="true"><span style="--i:${i}">${w}</span></span>`)
      .join(' ');
  });

  const state = { step: null, shown: null, lock: null };
  let lockTimer = 0;
  let fallbackTimer = 0;

  function leave(a) {
    clearTimeout(a._t);
    if (!a.classList.contains('is-active')) return;
    a.classList.remove('is-active');
    a.classList.add('is-leaving');
    a._t = setTimeout(() => a.classList.remove('is-leaving'), 800);
  }

  function enter(step) {
    if (step !== state.step || state.shown === step) return;
    state.shown = step;
    if (step < 0) return;
    const a = articles[step];
    clearTimeout(a._t);
    a.classList.remove('is-leaving');
    void a.offsetWidth; // restart transitions from the hidden pose
    a.classList.add('is-active');
  }

  const stage = new VideoStage([...camera.querySelectorAll('video')], enter);

  /* ---------------------------------------------------------------
     3. Scroll controller
     p = how many screens we are into the showcase.
       p < 0.5          → hero (step -1)
       0.5 + i ≤ p      → service i (one screen each)
     --------------------------------------------------------------- */
  function setStep(step) {
    if (step === state.step) return;
    state.step = step;
    state.shown = null;
    articles.forEach(leave);
    stage.goTo(step);
    clearTimeout(fallbackTimer);
    fallbackTimer = setTimeout(() => enter(step), CONFIG.textFallback);
  }

  let heroP = 0;
  function onScroll() {
    const vh = stageEl.offsetHeight;
    const p = -showcase.getBoundingClientRect().top / vh;

    // Hero leaves with a little extra depth; services UI fades in
    heroP = clamp(p, 0, 1);
    hero.style.setProperty('--hero-p', reduceMotion.matches ? 0 : heroP.toFixed(4));
    hero.style.opacity = reduceMotion.matches ? String(1 - clamp(p * 2, 0, 1)) : '';
    const uiO = clamp((p - 0.3) / 0.3, 0, 1);
    ui.style.setProperty('--ui', uiO.toFixed(3));
    ui.classList.toggle('is-on', uiO > 0.5);

    // Glass nav: "Services" is active while the showcase is pinned, "Home" otherwise
    const navKey = p >= 0.5 && p < STEPS + 0.5 ? 'services' : 'home';
    if (navKey !== state.nav && window.VSQC && VSQC.setNav) { state.nav = navKey; VSQC.setNav(navKey); }

    const step = p < 0.5 ? -1 : clamp(Math.floor(p - 0.5), 0, STEPS - 1);
    if (state.lock !== null) {
      if (step !== state.lock) return;    // passing through steps during a jump
      state.lock = null;
    }
    setStep(step);
  }

  function unlock() {
    if (state.lock === null) return;
    clearTimeout(lockTimer);
    state.lock = null;
    onScroll();
  }
  // The user taking over the scroll mid-jump ends the jump
  ['wheel', 'touchstart', 'keydown'].forEach((ev) => addEventListener(ev, unlock, { passive: true }));

  /* Scroll so that `step` is centred in its range. Far jumps skip
     the intermediate transitions (crossfade straight to the target). */
  function scrollToStep(step) {
    const top = showcase.getBoundingClientRect().top + scrollY;
    const y = top + (step + 1) * stageEl.offsetHeight;
    const far = state.step === null || Math.abs(step - state.step) > 1;
    if (far) {
      state.lock = step;
      setStep(step);
      clearTimeout(lockTimer);
      lockTimer = setTimeout(unlock, 5000);            // safety net if the scroll is interrupted
    }
    const lenis = window.VSQC && VSQC.lenis;
    if (lenis) {
      lenis.scrollTo(y, {
        duration: far ? 1.8 : 1.4,
        easing: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
        onComplete: far ? unlock : undefined,
      });
    } else {
      scrollTo({ top: y, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
      if (far) addEventListener('scrollend', unlock, { once: true });
    }
  }

  document.querySelectorAll('[data-scroll-step]').forEach((a) =>
    a.addEventListener('click', (e) => {
      e.preventDefault();
      if (window.VSQC && VSQC.closeMenu) VSQC.closeMenu();
      scrollToStep(Number(a.dataset.scrollStep));
    })
  );

  /* ---------------------------------------------------------------
     5. Camera — slow dolly-in as the hero hands over, plus a gentle
        pointer-driven tilt. Transform only (GPU), smoothed per frame.
     --------------------------------------------------------------- */
  const cam = { x: 0, y: 0, tx: 0, ty: 0 };
  addEventListener('pointermove', (e) => {
    if (!finePointer.matches || reduceMotion.matches) return;
    cam.tx = e.clientX / innerWidth - 0.5;
    cam.ty = e.clientY / innerHeight - 0.5;
  }, { passive: true });

  const ease = (t) => 1 - Math.pow(1 - t, 3);
  const narrow = matchMedia('(max-width: 820px)');
  const pullbackFor = () => (narrow.matches ? 0.1 : 0.07);
  let camPullback = pullbackFor();
  narrow.addEventListener('change', () => { camPullback = pullbackFor(); });
  function tick() {
    if (stage.active && !reduceMotion.matches) {
      cam.x += (cam.tx - cam.x) * 0.045;
      cam.y += (cam.ty - cam.y) * 0.045;
      // Camera pulls back a touch as the hero hands over, so tall towers clear the nav
      const s = 1 - camPullback * ease(heroP);
      camera.style.transform =
        `translate3d(${(-cam.x * 16).toFixed(2)}px, ${(-cam.y * 10).toFixed(2)}px, 0) ` +
        `rotateY(${(cam.x * 2.2).toFixed(3)}deg) rotateX(${(-cam.y * 1.5).toFixed(3)}deg) scale(${s.toFixed(4)})`;
    }
    requestAnimationFrame(tick);
  }

  /* ---------------------------------------------------------------
     6. Visibility + start-up (nav, menu and smooth scroll live in site.js)
     --------------------------------------------------------------- */
  // Pause videos when the showcase is off screen or the tab is hidden
  new IntersectionObserver(([e]) => stage.setActive(e.isIntersecting && !document.hidden))
    .observe(showcase);
  document.addEventListener('visibilitychange', () => {
    const r = showcase.getBoundingClientRect();
    stage.setActive(!document.hidden && r.bottom > 0 && r.top < innerHeight);
  });

  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);

  // Arriving from another page via index.html#services → open on service 1
  if (location.hash === '#services') {
    history.replaceState(null, '', location.pathname);
    const y = showcase.offsetTop + stageEl.offsetHeight;
    const lenis = window.VSQC && VSQC.lenis;
    if (lenis) lenis.scrollTo(y, { immediate: true, force: true });
    else scrollTo(0, y);
  }
  onScroll();
  requestAnimationFrame(tick);
})();
