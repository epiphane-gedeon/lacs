// Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on links
document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}));

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 100; // Account for floating header
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Testimonials Carousel
class TestimonialsCarousel {
    constructor() {
        this.currentSlide = 0;
        this.totalSlides = 3;
        this.avatarItems = document.querySelectorAll('.avatar-item');
        this.messageContents = document.querySelectorAll('.message-content');
        this.dots = document.querySelectorAll('.nav-dot');
        this.carousel = document.querySelector('.avatars-carousel');

        this.init();
    }

    init() {
        // Marquer l'état initial
        this.updateCarousel();

        // Auto-play carousel
        this.autoPlay = setInterval(() => {
            this.nextSlide();
        }, 5000);

        // Add click event to dots
        this.dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                this.goToSlide(index);
            });
        });

        // Add click events to avatars
        this.avatarItems.forEach((avatar, index) => {
            avatar.addEventListener('click', () => {
                this.goToSlide(index);
            });
        });

        // Pause auto-play on hover
        if (this.carousel) {
            this.carousel.addEventListener('mouseenter', () => {
                clearInterval(this.autoPlay);
            });

            this.carousel.addEventListener('mouseleave', () => {
                this.autoPlay = setInterval(() => {
                    this.nextSlide();
                }, 5000);
            });
        }
    }

    updateCarousel() {
        // Mettre à jour la classe du carrousel pour les positions
        this.carousel.className = `avatars-carousel active-${this.currentSlide}`;

        // Mettre à jour les avatars actifs
        this.avatarItems.forEach((avatar, index) => {
            avatar.classList.toggle('active', index === this.currentSlide);
        });

        // Mettre à jour les messages
        this.messageContents.forEach((message, index) => {
            message.classList.toggle('active', index === this.currentSlide);
        });

        // Mettre à jour les dots
        this.dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentSlide);
        });
    }

    goToSlide(slideIndex) {
        if (slideIndex === this.currentSlide) return;

        this.currentSlide = slideIndex;
        this.updateCarousel();
    }

    nextSlide() {
        const nextIndex = (this.currentSlide + 1) % this.totalSlides;
        this.goToSlide(nextIndex);
    }

    previousSlide() {
        const prevIndex = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
        this.goToSlide(prevIndex);
    }
}// Statistics Animation
const animateStats = () => {
    const stats = document.querySelectorAll('.stat-number');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = target.textContent;

                // Extract number from text (handle percentage and decimal)
                const numericValue = parseFloat(finalValue.replace(/[^\d.]/g, ''));
                const isPercentage = finalValue.includes('%');
                const hasDecimal = finalValue.includes('.');

                // Animate the number
                let currentValue = 0;
                const increment = numericValue / 50; // 50 steps
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= numericValue) {
                        currentValue = numericValue;
                        clearInterval(timer);
                    }

                    let displayValue;
                    if (hasDecimal) {
                        displayValue = currentValue.toFixed(1);
                    } else {
                        displayValue = Math.floor(currentValue);
                    }

                    target.textContent = displayValue + (isPercentage ? '%' : '') +
                        (finalValue.includes('/5') ? '/5' : '');
                }, 50);

                observer.unobserve(target);
            }
        });
    });

    stats.forEach(stat => observer.observe(stat));
};

// Contact Form Handler
const handleContactForm = () => {
    const form = document.getElementById('contactForm');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);
        const name = formData.get('name');
        const email = formData.get('email');
        const subject = formData.get('subject');
        const message = formData.get('message');

        // Simple validation
        if (!name || !email || !subject || !message) {
            showNotification('Veuillez remplir tous les champs', 'error');
            return;
        }

        if (!isValidEmail(email)) {
            showNotification('Veuillez entrer une adresse email valide', 'error');
            return;
        }

        // Simulate form submission
        showNotification('Message envoyé avec succès !', 'success');
        form.reset();
    });
};

// Email validation
const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

// Notification system
const showNotification = (message, type) => {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        ${type === 'success' ? 'background: #28a745;' : 'background: #dc3545;'}
    `;

    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
};

// Navbar scroll effect
const handleNavbarScroll = () => {
    const navbar = document.querySelector('.header');
    let lastScrollTop = 0;

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 10) {
            // Menu avec effet glass dès le début du scroll
            navbar.classList.add('glass-effect');
        } else {
            // Menu transparent en haut de page
            navbar.classList.remove('glass-effect');
        }

        lastScrollTop = scrollTop;
    });
};

// Scroll animations for sections
const handleScrollAnimations = () => {
    const animatedElements = document.querySelectorAll('.news-card, .about-text, .contact-info');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
};

// Inscription button handler
const handleInscriptionButton = () => {
    const inscriptionBtn = document.querySelector('.inscription-btn');

    inscriptionBtn.addEventListener('click', () => {
        // You can replace this with actual registration logic
        window.location.href = 'inscription.html';
        showNotification('Redirection vers la page d\'inscription...', 'success');

        // Simulate redirect after 2 seconds
        setTimeout(() => {
            // window.location.href = '/inscription';
            console.log('Redirect to inscription page');
        }, 2000);
    });
};

// CTA buttons handlers
const handleCTAButtons = () => {
    const primaryBtn = document.querySelector('.btn-primary');
    const secondaryBtn = document.querySelector('.btn-secondary');

    if (primaryBtn) {
        primaryBtn.addEventListener('click', () => {
            document.querySelector('#contact').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }

    if (secondaryBtn) {
        secondaryBtn.addEventListener('click', () => {
            showNotification('Redirection vers le formulaire de devis...', 'success');
        });
    }
};

// News buttons handler
const handleNewsButtons = () => {
    const newsButtons = document.querySelectorAll('.news-btn');

    newsButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const articleId = e.target.getAttribute('data-article');

            // URLs des articles
            const articleUrls = {
                'presco-2025-2026': 'activites-prescolaires.html',
                'invitation-bourse': 'bourse.html', // À créer plus tard
                'ateliers-ete': '#' // À créer plus tard
            };

            if (articleUrls[articleId] && articleUrls[articleId] !== '#') {
                // Redirection vers la page d'article
                window.location.href = articleUrls[articleId];
            } else if (articleUrls[articleId] === '#') {
                // Articles pas encore créés
                showNotification(`Article "${getArticleTitle(articleId)}" en cours de rédaction`, 'success');
            } else {
                showNotification('Article non trouvé', 'error');
            }
        });
    });
};

// Helper function to get article titles
const getArticleTitle = (articleId) => {
    const titles = {
        'bac-2025': 'Nouveau programme de préparation au Bac 2025',
        'olympiades-physique': 'Nos élèves brillent aux olympiades de physique',
        'ateliers-ete': 'Ateliers d\'été : Sciences et Innovation'
    };
    return titles[articleId] || 'Article';
};

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize carousel
    new TestimonialsCarousel();

    // Initialize other features
    animateStats();
    handleContactForm();
    handleNavbarScroll();
    handleScrollAnimations();
    handleInscriptionButton();
    handleCTAButtons();
    handleNewsButtons();

});

// Add some interactive features for better UX
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects to cards
    const cards = document.querySelectorAll('.news-card, .stat-item');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .inscription-btn, .news-btn');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;

            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add CSS for ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});
