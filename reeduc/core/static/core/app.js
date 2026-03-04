/**
 * ESPI – Shared application JavaScript
 * Sidebar toggles, user menu, quick-add, search autocomplete
 */
document.addEventListener('DOMContentLoaded', () => {

    /* ── Sidebar collapse toggle ── */
    const sidebar      = document.getElementById('sidebar');
    const collapseBtn  = document.getElementById('sidebarCollapseBtn');
    const mobileToggle = document.getElementById('mobileToggle');

    if (collapseBtn) {
        collapseBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
        });
        // Restore state
        if (localStorage.getItem('sidebar-collapsed') === 'true') {
            sidebar.classList.add('collapsed');
        }
    }

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('mobile-open');
        });
    }

    // Close mobile sidebar when clicking outside
    document.addEventListener('click', (e) => {
        if (sidebar && sidebar.classList.contains('mobile-open') &&
            !sidebar.contains(e.target) && e.target !== mobileToggle) {
            sidebar.classList.remove('mobile-open');
        }
    });

    /* ── Nav sub-menu toggles ── */
    document.querySelectorAll('.nav-item--toggle').forEach(btn => {
        const targetId = btn.getAttribute('data-target');
        const submenu  = document.getElementById(targetId);
        if (!submenu) return;

        // Auto-open if current URL matches a sub-item
        const currentPath = window.location.pathname;
        const links = submenu.querySelectorAll('a');
        let isActive = false;
        links.forEach(link => {
            if (currentPath.startsWith(link.getAttribute('href'))) {
                isActive = true;
                link.classList.add('active');
            }
        });
        if (isActive) {
            submenu.classList.add('is-open');
            btn.setAttribute('aria-expanded', 'true');
            btn.classList.add('active');
        }

        btn.addEventListener('click', () => {
            const open = submenu.classList.toggle('is-open');
            btn.setAttribute('aria-expanded', open);
        });
    });

    // Highlight active nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar__nav > a.nav-item').forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath === href) {
            item.classList.add('active');
        }
    });

    /* ── Quick-add menu ── */
    const quickAddBtn  = document.getElementById('quickAddBtn');
    const quickAddMenu = document.getElementById('quickAddMenu');

    if (quickAddBtn && quickAddMenu) {
        quickAddBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            quickAddMenu.classList.toggle('is-open');
        });
    }

    /* ── User dropdown ── */
    const userToggle   = document.getElementById('userMenuToggle');
    const userDropdown = document.getElementById('userMenuDropdown');

    if (userToggle && userDropdown) {
        userToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('is-open');
        });
    }

    // Close dropdowns on outside clicks
    document.addEventListener('click', (e) => {
        if (quickAddMenu && !quickAddBtn.contains(e.target)) {
            quickAddMenu.classList.remove('is-open');
        }
        if (userDropdown && !userToggle.contains(e.target) && !userDropdown.contains(e.target)) {
            userDropdown.classList.remove('is-open');
        }
    });

    /* ── Search autocomplete ── */
    const searchBoxes = document.querySelectorAll('.topbar__search');
    if (!searchBoxes.length) return;

    const buildResults = (container) => {
        const results = document.createElement('div');
        results.className = 'search-results';
        results.style.display = 'none';
        container.appendChild(results);
        return results;
    };

    const fetchResults = async (query) => {
        const response = await fetch(`/agendamentos/buscar?q=${encodeURIComponent(query)}`);
        if (!response.ok) return [];
        const data = await response.json();
        return data.results || [];
    };

    searchBoxes.forEach((box, index) => {
        const input = box.querySelector('input');
        if (!input) return;
        if (!input.id) {
            input.id = index === 0 ? 'mainSearch' : `mainSearch-${index}`;
        }
        input.setAttribute('autocomplete', 'off');
        const results = buildResults(box);

        const closeResults = () => {
            results.style.display = 'none';
            results.innerHTML = '';
        };

        input.addEventListener('input', async () => {
            const query = input.value.trim();
            if (query.length < 2) { closeResults(); return; }
            const items = await fetchResults(query);
            results.innerHTML = '';
            if (!items.length) { closeResults(); return; }
            items.forEach((item) => {
                const row = document.createElement('div');
                row.className = 'search-result-item';
                row.textContent = item.text;
                row.addEventListener('click', () => {
                    window.location.href = `/cadastro/perfil/${item.id}`;
                });
                results.appendChild(row);
            });
            results.style.display = 'block';
        });

        document.addEventListener('click', (e) => {
            if (!box.contains(e.target)) closeResults();
        });
    });

});
