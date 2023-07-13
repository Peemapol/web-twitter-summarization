function animateCounter(element) {
    element.innerText = '0';
  
    const target = parseInt(element.getAttribute('data-target'));
    const increment = target / 250;
  
    const updateCounter = () => {
      const currentValue = parseInt(element.innerText);
  
      if (currentValue < target) {
        element.innerText = Math.ceil(currentValue + increment);
        setTimeout(updateCounter, 1);
      } else {
        element.innerText = target.toLocaleString();
      }
    };
  
    updateCounter();
  }
  
  function onIntersection(entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        
        animateCounter(entry.target);
        observer.unobserve(entry.target); // Stop observing the element after animation
      }
    });
  }
  
  const observer = new IntersectionObserver(onIntersection, { threshold: 0.5 });
  
  function observeElements() {
    const counters = document.querySelectorAll('.retweet-number');
  
    counters.forEach((counter) => {
      observer.observe(counter);
    });
  }
  
  observeElements(); // Initial observation
  
  setInterval(() => {
    const newCounters = document.querySelectorAll('.retweet-number:not(.observed)');
    newCounters.forEach((counter) => {
      counter.classList.add('observed');
      observer.observe(counter);
    });
  }, 1000);
