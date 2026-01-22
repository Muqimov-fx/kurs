document.addEventListener('DOMContentLoaded', () => {
    // Service selection logic
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('click', () => {
            card.classList.toggle('selected');
            const checkbox = card.querySelector('input[type="checkbox"]');
            if (checkbox) {
                checkbox.checked = !checkbox.checked;
            }
        });
    });

    // Wizard navigation (Mock logic for frontend demo)
    const nextBtns = document.querySelectorAll('.btn-next');
    const steps = document.querySelectorAll('.step-content');
    const indicators = document.querySelectorAll('.step');
    let currentStep = 0;

    nextBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep === 0) {
                // Step 1 validation and data copy
                const emailInput = document.getElementById('eri-email');
                if (emailInput && emailInput.value) {
                    const confirmEmail = document.getElementById('confirm-email');
                    if (confirmEmail) confirmEmail.innerText = emailInput.value;
                }
            }

            if (currentStep < steps.length - 1) {
                steps[currentStep].style.display = 'none';
                currentStep++;
                steps[currentStep].style.display = 'block';
                steps[currentStep].classList.add('animate-fade-in');
                updateIndicators();
            }
        });
    });

    function updateIndicators() {
        indicators.forEach((indicator, index) => {
            if (index < currentStep) {
                indicator.classList.add('completed');
                indicator.classList.remove('active');
            } else if (index === currentStep) {
                indicator.classList.add('active');
                indicator.classList.remove('completed');
            } else {
                indicator.classList.remove('active', 'completed');
            }
        });
    }

    // Mock ERi generation with Backend Call
    const generateBtn = document.querySelector('#generate-eri-btn');
    if (generateBtn) {
        generateBtn.addEventListener('click', () => {
            const btnText = generateBtn.innerText;
            generateBtn.innerText = 'Generatsiya qilinmoqda...';
            generateBtn.disabled = true;

            // Call Backend API to create key
            fetch('/api/generate-key', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        setTimeout(() => {
                            document.querySelector('#wizard-step-3').style.display = 'none';
                            const successStep = document.querySelector('#wizard-step-success');
                            successStep.style.display = 'block';
                            successStep.classList.add('animate-fade-in');

                            // Update download link
                            const downloadBtn = successStep.querySelector('a');
                            downloadBtn.href = data.file_url;

                            // Update filename display
                            const fileBadge = successStep.querySelector('.glass');
                            fileBadge.innerHTML = `<i class="fas fa-file-code"></i> ${data.key_id}.pfx`;

                            confettiEffect();
                        }, 1500);
                    }
                })
                .catch(err => {
                    console.error("Error creating key:", err);
                    generateBtn.innerText = "Xatolik! Qayta urinib ko'ring";
                    generateBtn.disabled = false;
                });
        });
    }
});

// Real-time Activity Clock
function updateClock() {
    const activitySpan = document.getElementById('last-activity');
    if (activitySpan) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        activitySpan.innerHTML = `Bugun, ${timeString}`;
    }
}
setInterval(updateClock, 1000);
updateClock(); // Initial call

// Confetti
function confettiEffect() {
    // Simple confetti mock using emojis if canvas library not present
    // For a real app, use canvas-confetti
    console.log("Confetti!");
}
