// Smooth scroll for navigation links
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Highlight active section in navigation
document.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('main section');
    const navLinks = document.querySelectorAll('.nav-links a');

    let currentSection = null;
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        if (pageYOffset >= sectionTop - sectionHeight / 3) {
            currentSection = section;
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (currentSection && link.getAttribute('href') === `#${currentSection.id}`) {
            link.classList.add('active');
        }
    });
});

async function getVisitorCount() {
    const response = await fetch("https://6w4gka72i7.execute-api.eu-west-1.amazonaws.com");
    const data = await response.json();
    document.getElementById("visitor-count").innerText = data.visitor_count;
  }
  getVisitorCount();