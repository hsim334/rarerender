document.addEventListener('DOMContentLoaded', () => {
    // 1. Magnetic Buttons
    const buttons = document.querySelectorAll('.btn-premium, .btn-secondary');
    
    buttons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const deltaX = (x - centerX) / 8; // Strength of pull
            const deltaY = (y - centerY) / 8;
            
            btn.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        });
        
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });

    // 2. Smooth Reveal on Scroll (Enhanced)
    const observerOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                // Optional: Stop observing once revealed
                revealObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px) scale(0.98)';
        el.style.transition = 'all 1s cubic-bezier(0.16, 1, 0.3, 1)';
        revealObserver.observe(el);
    });

    // Add active class style dynamically if not in CSS
    const style = document.createElement('style');
    style.textContent = `
        .reveal.active {
            opacity: 1 !important;
            transform: translateY(0) scale(1) !important;
        }
    `;
    document.head.appendChild(style);
});
