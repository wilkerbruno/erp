document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.getElementById('sidebar');
    var mainContent = document.getElementById('mainContent');
    var topHeader = document.getElementById('topHeader');
    var mobileToggle = document.getElementById('mobileToggle');
    var sidebarOverlay = document.getElementById('sidebarOverlay');

    function openMenu() {
        sidebar.classList.add('show');
        sidebar.classList.remove('hidden');
        sidebarOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
        sidebar.classList.remove('show');
        sidebar.classList.add('hidden');
        sidebarOverlay.classList.remove('active');
        document.body.style.overflow = '';
        if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'false');
    }

    function toggleMenu() {
        if (sidebar.classList.contains('show')) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    if (mobileToggle) {
        mobileToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleMenu();
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeMenu);
    }

    var navLinks = sidebar ? sidebar.querySelectorAll('.nav-link') : [];
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                setTimeout(closeMenu, 150);
            }
        });
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeMenu();
            sidebar.classList.remove('hidden', 'show');
            document.body.style.overflow = '';
        }
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('show')) {
            closeMenu();
        }
    });

    if (window.innerWidth <= 768) {
        sidebar.classList.add('hidden');
        if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'false');
    }

    var currentPath = window.location.pathname;
    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
            alertInstance.close();
        });
    }, 5000);

    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});

window.mostrarAlerta = function(tipo, mensagem) {
    var container = document.querySelector('.content-wrapper');
    if (!container) return;
    var alerta = document.createElement('div');
    alerta.className = 'alert alert-' + tipo + ' alert-dismissible fade show';
    alerta.innerHTML = mensagem.replace(/\n/g, '<br>') +
        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
    container.insertBefore(alerta, container.firstChild);
    setTimeout(function() { alerta.remove(); }, 5000);
};

window.showAlert = window.mostrarAlerta;

window.toggleLoading = function(element, loading) {
    if (typeof loading === 'undefined') loading = true;
    if (loading) {
        element.classList.add('loading');
        element.disabled = true;
    } else {
        element.classList.remove('loading');
        element.disabled = false;
    }
};