/* Original class-based interactions, with safe DOM and keyboard boundaries. */
function switchClass(eid, cname) {
    const target = document.getElementById(eid);
    if (!target) return false;
    target.classList.toggle(cname);
    return true;
}

function updateNavigation() {
    const nav = document.getElementById('floatNav');
    if (!nav) return;
    const mobile = window.matchMedia('(max-width: 1024px)').matches;
    const opened = nav.classList.contains('nav-active');
    nav.inert = mobile && !opened;
    nav.setAttribute('aria-hidden', String(mobile && !opened));
    document.querySelectorAll('[aria-controls="floatNav"]').forEach(control => {
        control.setAttribute('aria-expanded', String(opened));
    });
}

function switchNav() {
    if (!switchClass('floatNav', 'nav-active')) return;
    updateNavigation();
    const nav = document.getElementById('floatNav');
    if (!nav.classList.contains('nav-active')) {
        const trigger = document.querySelector('.nav-trigger [role="button"]');
        if (trigger) trigger.focus();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[role="button"][onclick]').forEach(control => {
        control.addEventListener('keydown', event => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                control.click();
            }
        });
    });
    document.addEventListener('keydown', event => {
        const nav = document.getElementById('floatNav');
        if (event.key === 'Escape' && nav && nav.classList.contains('nav-active')) switchNav();
    });
    window.addEventListener('resize', updateNavigation);
    updateNavigation();
});
