// Mobile navigation toggle: adds accessible open/close, Esc to close, and outside-click close.
(function () {
    function initMobileNav() {
        const btn = document.getElementById('mobileMenuBtn');
        const nav = document.getElementById('mobileNav');
        if (!btn || !nav) return;

        function openNav() {
            nav.classList.remove('hidden');
            btn.setAttribute('aria-expanded', 'true');
            document.documentElement.classList.add('overflow-hidden');
        }

        function closeNav() {
            nav.classList.add('hidden');
            btn.setAttribute('aria-expanded', 'false');
            document.documentElement.classList.remove('overflow-hidden');
        }

        btn.addEventListener('click', function (e) {
            const expanded = btn.getAttribute('aria-expanded') === 'true';
            if (expanded) closeNav(); else openNav();
        });

        // Close on Esc
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeNav();
        });

        // Close clicking outside the nav on small screens
        document.addEventListener('click', function (e) {
            if (nav.classList.contains('hidden')) return;
            const target = e.target;
            if (!nav.contains(target) && !btn.contains(target)) {
                closeNav();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileNav);
    } else {
        initMobileNav();
    }
})();
