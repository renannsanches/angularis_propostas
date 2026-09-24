const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
function openTarget(id, focus = false) {
  const target = document.getElementById(id);
  if (!target) return;
  let node = target;
  while (node) { if (node.tagName === 'DETAILS') node.open = true; node = node.parentElement; }
  if (focus && target.matches('[tabindex]')) target.focus({ preventScroll: true });
}
document.querySelectorAll('a[data-scope]').forEach(link => link.addEventListener('click', () => openTarget(link.hash.slice(1), true)));
window.addEventListener('hashchange', () => openTarget(location.hash.slice(1)));
openTarget(location.hash.slice(1));
document.querySelectorAll('.collapse-document').forEach(button => {
  button.addEventListener('click', () => {
    const details = button.closest('details'); details.open = false;
    const summary = details.querySelector('summary'); summary.focus({ preventScroll: true });
    summary.scrollIntoView({ behavior: reduceMotion.matches ? 'instant' : 'smooth', block: 'start' });
  });
});
// The page remains readable before enhancement and if scripts are unavailable.
if (window.gsap && window.ScrollTrigger) {
  gsap.registerPlugin(ScrollTrigger);
  const motion = gsap.matchMedia();
  motion.add('(prefers-reduced-motion: no-preference)', context => {
    const intro = gsap.timeline({ defaults: { ease: 'expo.out', duration: 1.1 } });
    intro.from('.hero-copy h1', { y: 18, opacity: 0.65, clearProps: 'all' })
      .from('.hero-copy .intro, .hero-actions', { y: 12, opacity: 0.7, stagger: 0.09, clearProps: 'all' }, 0.12);

    // Reveal each reading group once, without hiding content before scripts run.
    // Animate package contents rather than its container, which may be pinned.
    const revealGroups = gsap.utils.toArray([
      '.section-heading', 'main > section:not(.hero) > h2',
      'main > section:not(.hero) > .lead', '.plan', '.deliverable',
      '.package > h3', '.package > .price', '.payment', '.journey > div',
      '.steps > article', '.conditions > div', '.documents > details',
      '.closing > div', '.closing > ol'
    ].join(','));
    const pending = revealGroups.filter(element => element.getBoundingClientRect().top > window.innerHeight);
    pending.forEach(element => element.dataset.scrollReveal = 'pending');
    gsap.set(pending, { opacity: 0, y: 16 });
    context.add('reveal', elements => {
      const entering = elements.filter(element => element.dataset.scrollReveal === 'pending');
      entering.forEach(element => element.dataset.scrollReveal = 'shown');
      gsap.to(entering, {
        opacity: 1, y: 0, duration: 0.7, ease: 'power3.out',
        stagger: { amount: Math.min(0.18, Math.max(0, entering.length - 1) * 0.06) },
        clearProps: 'opacity,transform', overwrite: 'auto'
      });
    });
    ScrollTrigger.batch(pending, {
      start: 'top 98%', once: true, interval: 0.06, batchMax: 5,
      onEnter: context.reveal,
      onEnterBack: context.reveal
    });
    const revealFocus = event => {
      const element = event.target.closest('[data-scroll-reveal]');
      if (!element) return;
      gsap.killTweensOf(element);
      gsap.set(element, { clearProps: 'opacity,transform' });
      element.dataset.scrollReveal = 'shown';
    };
    document.addEventListener('focusin', revealFocus);
    return () => {
      document.removeEventListener('focusin', revealFocus);
      pending.forEach(element => delete element.dataset.scrollReveal);
    };
  });
  motion.add('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)', () => {
    const cleanups = [...document.querySelectorAll('.plan, .package')].map(card => {
      let frame = 0;
      const move = event => {
        if (frame) cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
          const rect = card.getBoundingClientRect();
          card.style.setProperty('--light-x', `${event.clientX - rect.left}px`);
          card.style.setProperty('--light-y', `${event.clientY - rect.top}px`);
          frame = 0;
        });
      };
      const leave = () => {
        cancelAnimationFrame(frame);
        frame = 0;
        card.style.removeProperty('--light-x');
        card.style.removeProperty('--light-y');
      };
      card.addEventListener('pointermove', move, { passive: true });
      card.addEventListener('pointerleave', leave);
      return () => { leave(); card.removeEventListener('pointermove', move); card.removeEventListener('pointerleave', leave); };
    });
    return () => cleanups.forEach(cleanup => cleanup());
  });
  motion.add('(min-width: 1101px) and (min-height: 760px) and (prefers-reduced-motion: no-preference)', () => {
    gsap.fromTo('.hero-art img', { scale: 0.92, opacity: 1 }, {
      scale: 1, opacity: 0.35, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 0.7 }
    });
    const container = document.querySelector('.digital'); const summary = document.querySelector('.package');
    const travel = () => container.offsetHeight - summary.offsetHeight;
    if (travel() > 60) ScrollTrigger.create({ trigger: summary, start: 'top 112px', end: () => '+=' + Math.max(0, travel()), pin: true, pinSpacing: false, invalidateOnRefresh: true });
  });
  document.querySelectorAll('details').forEach(details => details.addEventListener('toggle', () => ScrollTrigger.refresh()));
  document.fonts.ready.then(() => ScrollTrigger.refresh());
}
if ('IntersectionObserver' in window) {
  const navigation = [...document.querySelectorAll('.navlinks a')];
  const observer = new IntersectionObserver(entries => {
    const section = entries.find(entry => entry.isIntersecting); if (!section) return;
    navigation.forEach(link => { if (link.hash === '#' + section.target.id) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
  }, { rootMargin: '-15% 0px -65% 0px', threshold: 0 });
  document.querySelectorAll('main > section[id]').forEach(section => observer.observe(section));
}
