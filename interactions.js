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
    // 3. Modal Logic
    const modal = document.getElementById('leadModal');
    const openBtns = document.querySelectorAll('.open-modal');
    const closeBtn = document.getElementById('closeModal');
    const leadForm = document.getElementById('leadForm');

    if (modal && openBtns.length > 0) {
        openBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            });
        });

        const closeModal = () => {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        };

        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

        if (leadForm) {
            leadForm.addEventListener('submit', async (e) => {
                e.preventDefault();

                const submitBtn = leadForm.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;

                // Multi-stage Feedback Sequence
                const stages = [
                    'Verifying Identity...',
                    'Securing Portfolio Access...',
                    'Access Granted!'
                ];

                let currentStage = 0;
                submitBtn.disabled = true;
                submitBtn.style.pointerEvents = 'none';
                submitBtn.style.opacity = '0.9';

                const updateStage = () => {
                    if (currentStage < stages.length) {
                        submitBtn.textContent = stages[currentStage];
                        currentStage++;
                        setTimeout(updateStage, 800);
                    }
                };

                updateStage();

                try {
                    const formData = new FormData(leadForm);
                    const response = await fetch(leadForm.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'Accept': 'application/json'
                        }
                    });

                    // We wait at least 2.5 seconds total for the psychological "Unlock" feeling
                    await new Promise(resolve => setTimeout(resolve, 2500));

                    if (response.ok) {
                        window.location.href = 'thank-you.html';
                    } else {
                        // Fallback redirect
                        window.location.href = 'thank-you.html';
                    }
                } catch (error) {
                    console.error('Error submitting form:', error);
                    window.location.href = 'thank-you.html';
                }
            });
        }
    }
});
