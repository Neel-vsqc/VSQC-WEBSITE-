/* ================================================================
   Service pages ("Blueprint" layout)
   1. Hero frame tilts gently with the pointer
   2. Step line draws down the page; each step lights as it's reached
   3. Go digital: particles gather into a certification seal when in view
   (standards tiles flip in via .rv / .in from site.js)
   ================================================================ */
(() => {
  'use strict';
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Hero frame tilt ---------- */
  const frame = document.querySelector('[data-tilt]');
  if (frame && !reduceMotion && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const hero = frame.closest('section');
    let tx = 0, ty = 0, x = 0, y = 0, raf = 0;
    const tick = () => {
      x += (tx - x) * 0.08;
      y += (ty - y) * 0.08;
      frame.style.transform = `rotateY(${(-12 + x * 14).toFixed(2)}deg) rotateX(${(4 - y * 10).toFixed(2)}deg)`;
      raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.001 ? requestAnimationFrame(tick) : 0;
    };
    hero.addEventListener('pointermove', (e) => {
      tx = e.clientX / innerWidth - 0.5;
      ty = e.clientY / innerHeight - 0.5;
      if (!raf) raf = requestAnimationFrame(tick);
    });
  }

  /* ---------- 2. Step line ---------- */
  const flow = document.querySelector('[data-flow]');
  if (flow) {
    const line = document.createElement('i');
    line.className = 'bp-flow__line';
    line.setAttribute('aria-hidden', 'true');
    flow.prepend(line);
    const rows = [...flow.querySelectorAll('.bp-row')];
    if (reduceMotion) {
      line.style.height = '100%';
      rows.forEach((r) => r.classList.add('is-lit'));
    } else {
      let ticking = false;
      const draw = () => {
        ticking = false;
        const r = flow.getBoundingClientRect();
        // the line's tip sits 60% down the screen
        const reach = Math.min(r.height, Math.max(0, innerHeight * 0.6 - r.top));
        line.style.height = `${reach}px`;
        rows.forEach((row) => row.classList.toggle('is-lit', row.offsetTop + row.offsetHeight / 2 <= reach));
      };
      addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(draw); } }, { passive: true });
      addEventListener('resize', draw);
      draw();
    }
  }

  /* ---------- 3. Particle seal ---------- */
  const seal = document.querySelector('[data-seal]');
  if (seal && seal.getContext) {
    const ctx = seal.getContext('2d');
    let W = 0, H = 0, dpr = 1, parts = [], formed = false, visible = false, raf = 0;
    const mouse = { x: -1e4, y: -1e4 };

    // Trace the seal (ring + tick) on a hidden canvas and keep a point wherever it is painted
    function targets(size) {
      const c = document.createElement('canvas');
      c.width = c.height = size;
      const g = c.getContext('2d');
      const m = size / 2;
      g.strokeStyle = '#fff';
      g.lineCap = g.lineJoin = 'round';
      g.lineWidth = size * 0.045;
      g.beginPath(); g.arc(m, m, size * 0.4, 0, Math.PI * 2); g.stroke();
      g.lineWidth = size * 0.012;
      g.beginPath(); g.arc(m, m, size * 0.31, 0, Math.PI * 2); g.stroke();
      g.lineWidth = size * 0.07;
      g.beginPath(); g.moveTo(size * 0.33, size * 0.52); g.lineTo(size * 0.45, size * 0.63); g.lineTo(size * 0.68, size * 0.38); g.stroke();
      const data = g.getImageData(0, 0, size, size).data;
      const gap = Math.max(5, Math.round(size / 52));
      const pts = [];
      for (let y = 0; y < size; y += gap) {
        for (let x = 0; x < size; x += gap) {
          if (data[(y * size + x) * 4 + 3] > 128) pts.push([x, y]);
        }
      }
      return pts;
    }

    function setup() {
      const r = seal.getBoundingClientRect();
      dpr = Math.min(2, window.devicePixelRatio || 1);
      W = r.width; H = r.height;
      seal.width = Math.round(W * dpr); seal.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const pts = targets(Math.round(W));
      const old = parts;
      parts = pts.map(([tx, ty], i) => {
        const p = old[i] || { x: W / 2, y: H / 2, vx: 0, vy: 0, s: 0.9 + Math.random() * 1.5, ph: Math.random() * 6.28 };
        p.tx = tx; p.ty = ty;
        const a = Math.random() * 6.283, rr = Math.sqrt(Math.random()) * W * 0.46;   // loose "drift" home inside a round cloud
        p.hx = W / 2 + Math.cos(a) * rr; p.hy = H / 2 + Math.sin(a) * rr;
        return p;
      });
      if (reduceMotion) { parts.forEach((p) => { p.x = p.tx; p.y = p.ty; }); paint(0); }
    }

    function paint(t) {
      ctx.clearRect(0, 0, W, H);
      for (const p of parts) {
        const glow = 0.6 + 0.4 * Math.sin(t / 900 + p.ph);
        ctx.fillStyle = `rgba(111, 211, 232, ${glow.toFixed(2)})`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.s, 0, 6.283); ctx.fill();
      }
    }

    function frame(t) {
      raf = 0;
      if (!visible) return;
      for (const p of parts) {
        // gathered: pull to the seal; loose: wander around a random home
        const gx = formed ? p.tx : p.hx + Math.sin(t / 1400 + p.ph) * 18;
        const gy = formed ? p.ty : p.hy + Math.cos(t / 1700 + p.ph) * 18;
        p.vx += (gx - p.x) * (formed ? 0.018 : 0.004);
        p.vy += (gy - p.y) * (formed ? 0.018 : 0.004);
        // the pointer pushes particles away
        const dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
        if (d2 < 2500) { const f = (2500 - d2) / 2500 * 2.2; const d = Math.sqrt(d2) || 1; p.vx += dx / d * f; p.vy += dy / d * f; }
        p.vx *= 0.86; p.vy *= 0.86;
        p.x += p.vx; p.y += p.vy;
      }
      paint(t);
      raf = requestAnimationFrame(frame);
    }
    const run = () => { if (!raf && !reduceMotion) raf = requestAnimationFrame(frame); };

    setup();
    addEventListener('resize', () => { setup(); run(); });
    seal.addEventListener('pointermove', (e) => { const r = seal.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    seal.addEventListener('pointerleave', () => { mouse.x = mouse.y = -1e4; });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        visible = entries[0].isIntersecting;
        // gather a moment after it comes into view
        if (visible && !formed) setTimeout(() => { formed = true; }, 600);
        run();
      }, { threshold: 0.35 }).observe(seal);
    } else {
      visible = formed = true; run();
    }
  }
})();
