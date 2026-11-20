/* Clients page: filter the logo wall by one or more industries, and search by name.
   Click industries to add/remove them (e.g. Automotive + IT shows both). "All" clears the selection. */
(() => {
  const wall = document.getElementById('all-clients');
  if (!wall) return;
  const groups = [...wall.querySelectorAll('.wall__group')];
  const featured = wall.querySelector('.wall__group--featured');
  const buttons = [...wall.querySelectorAll('.wall__filter')];
  const allBtn = buttons.find((b) => b.dataset.filter === 'all');
  const input = wall.querySelector('.wall__search input');
  const empty = wall.querySelector('.wall__empty');
  const others = wall.querySelector('.others');
  const otherGroups = [...wall.querySelectorAll('.others__group')];
  const picked = new Set();

  function render() {
    const q = (input.value || '').trim().toLowerCase();
    const all = picked.size === 0;
    let shown = 0;
    groups.forEach((g) => {
      const isFeatured = g === featured;
      // Featured row only on "All" with no search, so nothing shows twice
      const groupOn = isFeatured ? all && !q : all || picked.has(g.dataset.industry);
      let visible = 0;
      g.querySelectorAll('.tile').forEach((t) => {
        const hit = !q || t.dataset.name.includes(q);
        t.hidden = !hit;
        if (hit) visible++;
      });
      g.hidden = !groupOn || visible === 0;
      if (!g.hidden && !isFeatured) shown += visible;
    });
    // "Other clients" (names without a logo): same industry filter and search
    let otherShown = 0;
    otherGroups.forEach((g) => {
      const on = all || picked.has(g.dataset.industry);
      let first = true, visible = 0;
      g.querySelectorAll('li').forEach((li) => {
        const hit = on && (!q || li.dataset.name.includes(q));
        li.hidden = !hit;
        li.toggleAttribute('data-first', hit && first);
        if (hit) { first = false; visible++; }
      });
      g.hidden = visible === 0;
      otherShown += visible;
    });
    if (others) others.hidden = otherShown === 0;
    buttons.forEach((b) => b.setAttribute('aria-pressed', String(b === allBtn ? all : picked.has(b.dataset.filter))));
    empty.hidden = shown + otherShown > 0;
  }

  buttons.forEach((b) => b.addEventListener('click', () => {
    const f = b.dataset.filter;
    if (f === 'all') picked.clear();
    else if (picked.has(f)) picked.delete(f);
    else picked.add(f);
    render();
  }));
  input.addEventListener('input', render);
  render();
})();
