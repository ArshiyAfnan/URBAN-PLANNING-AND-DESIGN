window.onload = () => {
  const title = document.getElementById('main-title');
  const subtitle = document.querySelector('.subtitle');

  // Animate title
  setTimeout(() => {
    title.style.opacity = '1';
    title.style.transform = 'translateY(0)';
  }, 500);

  // Animate subtitle
  setTimeout(() => {
    subtitle.style.opacity = '1';
  }, 1200);
};

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();

    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});
