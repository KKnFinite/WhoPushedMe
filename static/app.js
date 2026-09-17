(() => {
  const splash = document.getElementById('launch-splash');
  const appShell = document.getElementById('app-shell');
  const modal = document.getElementById('construction-modal');
  const modalClose = document.getElementById('construction-close');
  const underConstructionButtons = document.querySelectorAll('[data-under-construction]');

  const revealApp = () => {
    if (splash) splash.classList.add('splash-leaving');
    window.setTimeout(() => {
      if (splash) splash.hidden = true;
      if (appShell) appShell.removeAttribute('aria-hidden');
      document.body.classList.add('app-ready');
    }, 260);
  };

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.setTimeout(revealApp, prefersReducedMotion ? 350 : 1450);

  const openConstruction = () => {
    if (!modal) return;
    modal.hidden = false;
    document.body.classList.add('modal-open');
    modalClose?.focus();
  };

  const closeConstruction = () => {
    if (!modal) return;
    modal.hidden = true;
    document.body.classList.remove('modal-open');
  };

  underConstructionButtons.forEach((button) => {
    button.addEventListener('click', openConstruction);
  });

  modalClose?.addEventListener('click', closeConstruction);
  modal?.addEventListener('click', (event) => {
    if (event.target === modal) closeConstruction();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modal && !modal.hidden) closeConstruction();
  });

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/service-worker.js').catch(() => {
        // The shell still works normally if service-worker registration fails.
      });
    });
  }
})();
