// Modern Portfolio JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    setupMobileMenu();
    
    // Smooth scrolling for navigation links
    setupSmoothScrolling();
    
    // Active navigation highlighting
    setupActiveNavigation();
    
    // Scroll reveal animations
    setupScrollReveal();
    
    // Scroll to top button
    setupScrollToTop();
    
    // Typing effect for hero title
    setupTypingEffect();
    
    // CV download loading animation
    setupCVDownloadAnimation();
    
    // Parallax effect for hero section
    setupParallaxEffect();
    
    // Skill animations
    setupSkillAnimations();
    
    // Hover effects
    setupHoverEffects();
    
    // Update copyright year
    updateCopyrightYear();
});

// Mobile Menu Setup
function setupMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('nav-open');
            
            // Update icon
            const icon = menuToggle.querySelector('i');
            if (navLinks.classList.contains('nav-open')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        });
        
        // Close menu when clicking on a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('nav-open');
                const icon = menuToggle.querySelector('i');
                icon.className = 'fas fa-bars';
            });
        });
    }
}

// Smooth Scrolling
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('.site-header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Active Navigation
function setupActiveNavigation() {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
    
    function updateActiveNav() {
        const scrollPos = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveNav);
    updateActiveNav(); // Initial call
}

// Scroll Reveal Animations
function setupScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationDelay = '0.1s';
                entry.target.style.animationPlayState = 'running';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll(
        '.section, .project-card, .experience-item, .education-item, .skill-group, .cert-item, .contact-card'
    );
    
    animatedElements.forEach(el => {
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });
}

// Scroll to Top Button
function setupScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.className = 'scroll-to-top';
    scrollButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollButton.setAttribute('aria-label', 'Scroll to top');
    document.body.appendChild(scrollButton);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollButton.classList.add('show');
        } else {
            scrollButton.classList.remove('show');
        }
    });
    
    // Scroll to top when clicked
    scrollButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Typing Effect
function setupTypingEffect() {
    const title = document.querySelector('.intro h1');
    if (!title) return;
    
    const text = title.textContent;
    title.textContent = '';
    title.style.borderRight = '3px solid var(--primary)';
    
    let i = 0;
    const typeWriter = () => {
        if (i < text.length) {
            title.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 100);
        } else {
            title.style.borderRight = 'none';
        }
    };
    
    // Start typing effect after a short delay
    setTimeout(typeWriter, 500);
}

// CV Download Animation
function setupCVDownloadAnimation() {
    const cvLinks = document.querySelectorAll('a[href*="Hamza_cv"]');
    
    cvLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Downloading...';
            this.style.pointerEvents = 'none';
            
            // Reset after animation
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.pointerEvents = 'auto';
            }, 2000);
        });
    });
}

// Parallax Effect
function setupParallaxEffect() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        hero.style.transform = `translateY(${rate}px)`;
    });
}

// Skill Animations
function setupSkillAnimations() {
    const skillGroups = document.querySelectorAll('.skill-group');
    
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const chips = entry.target.querySelectorAll('.chip');
                chips.forEach((chip, index) => {
                    setTimeout(() => {
                        chip.style.opacity = '1';
                        chip.style.transform = 'translateY(0)';
                    }, index * 100);
                });
            }
        });
    }, { threshold: 0.5 });
    
    skillGroups.forEach(group => {
        skillObserver.observe(group);
        
        // Set initial state for chips
        const chips = group.querySelectorAll('.chip');
        chips.forEach(chip => {
            chip.style.opacity = '0';
            chip.style.transform = 'translateY(20px)';
            chip.style.transition = 'all 0.5s ease';
        });
    });
}

// Hover Effects
function setupHoverEffects() {
    // Add hover effects to interactive elements
    const hoverElements = document.querySelectorAll(
        '.button, .project-card, .experience-item, .education-item, .skill-group, .cert-item, .contact-card, .highlight-item'
    );
    
    hoverElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Update Copyright Year
function updateCopyrightYear() {
    const yearElement = document.getElementById('year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

// Add loading animation for images
function setupImageLoading() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.5s ease';
    });
}

// Initialize image loading
setupImageLoading();

// Add some additional interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.button');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add CSS for ripple effect
    const style = document.createElement('style');
    style.textContent = `
        .button {
            position: relative;
            overflow: hidden;
        }
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});


