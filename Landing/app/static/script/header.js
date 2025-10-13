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

const handleInscriptionButton = () => {
    const inscriptionBtn = document.querySelector('.inscription-btn');

    if (inscriptionBtn) {
        inscriptionBtn.addEventListener('click', (e) => {
            // Le lien va déjà vers la bonne route Flask, pas besoin de redirection
            console.log('Redirection vers la page d\'inscription...');
        });
    }
};

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

document.addEventListener('DOMContentLoaded', () => {

    handleNavbarScroll();
    handleInscriptionButton();
});