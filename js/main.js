// ============================================
// FORGE 8 ATHLETICS — SHARED JS
// ============================================

document.addEventListener('DOMContentLoaded', () => {

  // --- CURSOR ---
  const cursor = document.getElementById('cursor');
  const ring   = document.getElementById('cursor-ring');
  if (cursor && ring && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    let mx = 0, my = 0, rx = 0, ry = 0;
    document.addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      cursor.style.left = mx + 'px';
      cursor.style.top  = my + 'px';
    });
    (function animateRing() {
      rx += (mx - rx) * 0.13;
      ry += (my - ry) * 0.13;
      ring.style.left = rx + 'px';
      ring.style.top  = ry + 'px';
      requestAnimationFrame(animateRing);
    })();
    document.querySelectorAll('a, button').forEach(el => {
      el.addEventListener('mouseenter', () => {
        cursor.style.width = '6px'; cursor.style.height = '6px';
        ring.style.width = '48px'; ring.style.height = '48px';
      });
      el.addEventListener('mouseleave', () => {
        cursor.style.width = '10px'; cursor.style.height = '10px';
        ring.style.width = '34px'; ring.style.height = '34px';
      });
    });
  }

  // --- NAV SCROLL ---
  const nav = document.querySelector('nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 60);
    });
  }

  // --- MOBILE NAV TOGGLE ---
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => navLinks.classList.remove('open'));
    });
  }

  // --- SCROLL REVEAL ---
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // --- ACTIVE NAV LINK ---
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href').split('/').pop();
    if (href === path) a.classList.add('active');
  });

  // --- LINK CLICK TRACKING ---
  if (typeof gtag === 'function') {
    const pageName = document.title.split('|')[0].trim();
    document.addEventListener('click', function(e) {
      const link = e.target.closest('a');
      if (!link) return;
      let text = link.innerText.trim().slice(0, 100);
      if (text === 'Join Now' || text === 'Claim Free Trial') {
        text = text + ' - ' + pageName;
      }
      gtag('event', 'link_click', {
        link_text: text,
        link_url: link.href
      });
    });
  }

});
