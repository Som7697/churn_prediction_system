// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded',function() {
const alerts = document.querySelectorAll('.alert');
alerts.forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Form validation
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#ef4444';
            } else {
                field.style.borderColor = '#e2e8f0';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('Please fill all required fields');
        }
    });
});
});
// Animate numbers on page load
function animateValue(element, start, end, duration) {
let startTimestamp = null;
const step = (timestamp) => {
if (!startTimestamp) startTimestamp = timestamp;
const progress = Math.min((timestamp - startTimestamp) / duration, 1);
element.textContent = Math.floor(progress * (end - start) + start);
if (progress < 1) {
window.requestAnimationFrame(step);
}
};
window.requestAnimationFrame(step);
}
// Initialize animations when elements are visible
const observer = new IntersectionObserver((entries) => {
entries.forEach(entry => {
if (entry.isIntersecting) {
entry.target.style.opacity = '1';
entry.target.style.transform = 'translateY(0)';
}
});
}, { threshold: 0.1 });
document.querySelectorAll('.stat-card, .feature-card, .action-btn').forEach(el => {
el.style.opacity = '0';
el.style.transform = 'translateY(20px)';
el.style.transition = 'all 0.6s ease';
observer.observe(el);
});