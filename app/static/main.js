function setupTryItOutHover() {
  document.querySelectorAll('.try-iy-out a').forEach(link => {
    const card = link.closest('.card');
    const title = card.querySelector('h3');
    const arrow = card.querySelector('.link-arrow');

    if (!title || !arrow) return;

    link.addEventListener('mouseenter', () => {
      title.classList.add('no-hover');
      arrow.classList.add('no-arrow-hover');
    });

    link.addEventListener('mouseleave', () => {
      title.classList.remove('no-hover');
      arrow.classList.remove('no-arrow-hover');
    });
  });
}

setupTryItOutHover();

document.body.addEventListener('htmx:afterSwap', (e) => {
  if (e.target.closest('#project-cards') || e.target.closest('#experience-cards')) {
    setupTryItOutHover();
  }
});

function scrollSpy() {
  const sections = document.querySelectorAll('main section');
  const navLinks = document.querySelectorAll('nav a[data-section]');

  function activateSection() {
    let current = "";

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      if (window.scrollY >= sectionTop - 400) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      link.parentElement.classList.remove('active');

      if (link.dataset.section === current) {
        link.classList.add('active');
        link.parentElement.classList.add('active');
      }
    });
  }

  window.addEventListener('scroll', activateSection);
  window.addEventListener('load', activateSection); // activa al cargar
}
scrollSpy();
