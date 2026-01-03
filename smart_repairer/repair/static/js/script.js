// Animated Number Counter
const counters = document.querySelectorAll('.stat-number');

const runCounter = (counter) => {
    const target = +counter.getAttribute('data-target');
    let count = 0;
    const speed = 200;
    
    const updateCount = () => {
        const increment = target / speed;
        
        if (count < target) {
            count += increment;
            counter.innerText = Math.ceil(count);
            setTimeout(updateCount, 1);
        } else {
            counter.innerText = target;
        }
    };
    
    updateCount();
};

const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            runCounter(entry.target);
            counterObserver.unobserve(entry.target);
        }
    });
}, { 
    threshold: 0.5
});

counters.forEach(counter => {
    counterObserver.observe(counter);
});

/* --- Sticky Nav --- */
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.navbar');
  nav.classList.toggle('sticky', window.scrollY > 0);
});

/* --- Smooth Scroll --- */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});