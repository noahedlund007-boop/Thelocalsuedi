(function () {
  var body = document.body, menu = document.getElementById('menu'), btn = document.querySelector('.burger');
  function setMenu(open) {
    if (open) menu.hidden = false;
    requestAnimationFrame(function () { menu.classList.toggle('on', open); });
    body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    body.style.overflow = open ? 'hidden' : '';
    if (!open) setTimeout(function () { if (!menu.classList.contains('on')) menu.hidden = true; }, 750);
  }
  btn.addEventListener('click', function () { setMenu(!menu.classList.contains('on')); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('on')) setMenu(false); });
  var sub = document.querySelector('.has-sub'), sb = sub.querySelector('button');
  sb.addEventListener('click', function () { var o = !sub.classList.contains('open'); sub.classList.toggle('open', o); sb.setAttribute('aria-expanded', String(o)); });
  menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { if (a.getAttribute('href').indexOf('#contact') > -1 && location.pathname.indexOf('about') > -1) setMenu(false); }); });

  // missing media -> neutral placeholder
  function miss(el) { var b = el.closest('.frame,.vid,.hero,.vframe'); if (b) b.classList.add('missing'); }
  document.addEventListener('error', function (e) { var t = e.target; if (t.tagName === 'IMG' || t.tagName === 'SOURCE') miss(t); }, true);
  document.querySelectorAll('img').forEach(function (i) { if (i.complete && i.naturalWidth === 0) miss(i); });

  // hover preview on index lists (desktop)
  var peek = document.querySelector('.peek'), pi = peek.querySelector('img');
  if (window.matchMedia('(hover:hover)').matches) {
    pi.addEventListener('error', function () { peek.classList.add('none'); });
    pi.addEventListener('load', function () { peek.classList.remove('none'); });
    document.querySelectorAll('.row').forEach(function (r) {
      r.addEventListener('mouseenter', function () { if (!r.dataset.img) return; pi.src = r.dataset.img; peek.classList.add('on'); });
      r.addEventListener('mouseleave', function () { peek.classList.remove('on'); });
    });
  }
  // YouTube loads only after the visitor presses play (no data sent to Google before that)
  document.querySelectorAll('.yt').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + b.dataset.id + '?autoplay=1&rel=0';
      f.title = b.dataset.title; f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen = true;
      b.replaceWith(f);
    });
  });
  // masonry: pictures keep their own proportions; each one goes into the shortest column, in the order of the page
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.masonry'));
  function layout(box) {
    var figs = box._f || (box._f = Array.prototype.slice.call(box.querySelectorAll('.f')).sort(function (a, b) { return a.dataset.i - b.dataset.i; }));
    var cs = getComputedStyle(box), w = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    var n = w >= 1400 ? 4 : w >= 900 ? 3 : 2, gap = w >= 700 ? 14 : 8;
    if (box._n === n && box._g === gap) return; box._n = n; box._g = gap;
    box.classList.add('on'); box.style.setProperty('--mg', gap + 'px');
    var cw = (w - gap * (n - 1)) / n, cols = [], hs = [], frag = document.createDocumentFragment();
    for (var c = 0; c < n; c++) { var col = document.createElement('div'); col.className = 'mcol'; cols.push(col); hs.push(0); frag.appendChild(col); }
    figs.forEach(function (f) {
      var r = parseFloat(f.style.getPropertyValue('--r')) || 1.5, k = 0;
      for (var c = 1; c < n; c++) if (hs[c] < hs[k] - 1) k = c;
      cols[k].appendChild(f); hs[k] += cw / r + gap;
    });
    while (box.firstChild) box.removeChild(box.firstChild); box.appendChild(frag);
  }
  boxes.forEach(layout);
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { boxes.forEach(layout); }, 150); });

  // lightbox: click a picture to see it large, browse with arrows / keys / swipe
  var figs = Array.prototype.slice.call(document.querySelectorAll('.f')).sort(function (a, b) { return a.dataset.i - b.dataset.i; });
  if (figs.length) {
    var sv = document.documentElement.lang === 'sv';
    var lab = sv ? { x: 'Stäng', p: 'Föregående bild', n: 'Nästa bild', d: 'Bildvisning', ph: 'Bilden är inte tillagd än' }
                 : { x: 'Close', p: 'Previous picture', n: 'Next picture', d: 'Picture viewer', ph: 'Picture not added yet' };
    var lb = document.createElement('div');
    lb.className = 'lb'; lb.hidden = true; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', lab.d);
    lb.innerHTML = '<button class="lb-x" type="button" aria-label="' + lab.x + '">&times;</button><button class="lb-nav lb-prev" type="button" aria-label="' + lab.p + '">&#8249;</button>' +
      '<button class="lb-nav lb-next" type="button" aria-label="' + lab.n + '">&#8250;</button><figure class="lb-fig"><div class="lb-stage"><img alt=""><div class="lb-ph"></div></div>' +
      '<figcaption><span class="lb-count" aria-live="polite"></span></figcaption></figure>';
    document.body.appendChild(lb);
    var limg = lb.querySelector('.lb-stage img'), lph = lb.querySelector('.lb-ph'), lcount = lb.querySelector('.lb-count');
    var btns = [lb.querySelector('.lb-x'), lb.querySelector('.lb-prev'), lb.querySelector('.lb-next')];
    var cur = 0, opener = null, isOpen = false;
    function show(i) {
      cur = (i + figs.length) % figs.length;
      var f = figs[cur], im = f.querySelector('img'), fr = f.querySelector('.frame');
      if (im.complete && im.naturalWidth > 0 && !fr.classList.contains('missing')) { limg.hidden = false; lph.hidden = true; limg.src = im.dataset.full || im.src; limg.alt = im.alt; }
      else { limg.hidden = true; lph.hidden = false; lph.textContent = lab.ph + ': ' + f.querySelector('.note').textContent.replace('Add image', '').trim(); }
      lcount.textContent = (cur + 1) + ' / ' + figs.length;
      [cur - 1, cur + 1].forEach(function (n) { var g = figs[(n + figs.length) % figs.length].querySelector('img'); if (g && g.src) new Image().src = g.src; });
    }
    function open(i) { opener = document.activeElement; isOpen = true; lb.hidden = false; document.body.style.overflow = 'hidden'; show(i); requestAnimationFrame(function () { lb.classList.add('on'); }); btns[0].focus(); }
    function close() { isOpen = false; lb.classList.remove('on'); document.body.style.overflow = ''; setTimeout(function () { if (!isOpen) lb.hidden = true; }, 300); if (opener) opener.focus(); }
    figs.forEach(function (f, i) {
      var fr = f.querySelector('.frame');
      fr.addEventListener('click', function () { open(i); });
      fr.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } });
    });
    btns[0].addEventListener('click', close);
    btns[1].addEventListener('click', function () { show(cur - 1); });
    btns[2].addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb-fig') || e.target.classList.contains('lb-stage')) close(); });
    document.addEventListener('keydown', function (e) {
      if (!isOpen) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(cur - 1);
      else if (e.key === 'ArrowRight') show(cur + 1);
      else if (e.key === 'Tab') { var i = btns.indexOf(document.activeElement); e.preventDefault(); btns[(i + (e.shiftKey ? -1 : 1) + btns.length) % btns.length].focus(); }
    });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); });
  }
  // film cards: player loads only after Play; description opens on demand
  document.querySelectorAll('.vplay').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = document.createElement('iframe'), id = b.dataset.id;
      f.src = b.dataset.k === 'yt' ? 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0' : 'https://www.instagram.com/reel/' + id + '/embed';
      f.title = b.dataset.title; f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen = true;
      b.parentNode.classList.add('playing'); b.replaceWith(f);
    });
  });
  document.querySelectorAll('.vmore').forEach(function (b) {
    var sv = document.documentElement.lang === 'sv', card = b.closest('.vc');
    b.addEventListener('click', function () {
      var o = !card.classList.contains('open'); card.classList.toggle('open', o); b.setAttribute('aria-expanded', String(o));
      b.textContent = o ? (sv ? 'Dölj beskrivning' : 'Hide description') : (sv ? 'Läs beskrivning' : 'Read description');
    });
  });
  var hv = document.querySelector('.hero video');
  if (hv && matchMedia('(prefers-reduced-motion:reduce)').matches) { hv.removeAttribute('autoplay'); hv.pause(); }
})();
