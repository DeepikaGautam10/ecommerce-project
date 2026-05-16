/* =========================================================
   Watch House - Main JavaScript
   Small progressive enhancements only. The site works
   fully without JS; this just improves the experience.
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {

    /* ---- Auto-dismiss flash messages after 5 seconds ---- */
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            if (window.bootstrap) {
                bootstrap.Alert.getOrCreateInstance(alert).close();
            }
        }, 5000);
    });

    /* ---- Auto-generate a URL slug from a name field ---- */
    var nameInput = document.querySelector('input[name="name"]');
    var slugInput = document.querySelector('input[name="slug"]');
    if (nameInput && slugInput) {
        nameInput.addEventListener('input', function () {
            // Only auto-fill while the slug has not been edited manually
            if (slugInput.dataset.touched === 'true') { return; }
            slugInput.value = this.value
                .toLowerCase()
                .trim()
                .replace(/[^a-z0-9\s-]/g, '')
                .replace(/\s+/g, '-')
                .replace(/-+/g, '-');
        });
        slugInput.addEventListener('input', function () {
            slugInput.dataset.touched = 'true';
        });
    }

    /* ---- Live image preview for file inputs ---- */
    document.querySelectorAll('input[type="file"]').forEach(function (input) {
        input.addEventListener('change', function (e) {
            var file = e.target.files[0];
            if (!file) { return; }
            var reader = new FileReader();
            reader.onload = function (ev) {
                var preview = input.parentElement.querySelector('.image-preview');
                if (!preview) {
                    preview = document.createElement('img');
                    preview.className = 'image-preview';
                    preview.alt = 'Image preview';
                    input.parentElement.appendChild(preview);
                }
                preview.src = ev.target.result;
            };
            reader.readAsDataURL(file);
        });
    });

    /* ---- Cart quantity stepper buttons ---- */
    document.querySelectorAll('[data-qty-step]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var target = document.getElementById(btn.dataset.target);
            if (!target) { return; }
            var value = parseInt(target.value, 10) || 1;
            var step = parseInt(btn.dataset.qtyStep, 10);
            var max = parseInt(target.getAttribute('max'), 10) || Infinity;
            var next = value + step;
            if (next >= 1 && next <= max) {
                target.value = next;
            }
        });
    });

    /* ---- Scroll-to-top button ---- */
    var scrollBtn = document.createElement('button');
    scrollBtn.type = 'button';
    scrollBtn.className = 'btn btn-primary scroll-top';
    scrollBtn.setAttribute('aria-label', 'Scroll to top');
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', function () {
        scrollBtn.style.display = window.scrollY > 350 ? 'flex' : 'none';
    });
    scrollBtn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    /* ---- Fade-in cards on load ---- */
    document.querySelectorAll('.product-card, .category-card').forEach(function (card, i) {
        card.style.animationDelay = (i % 8) * 60 + 'ms';
        card.classList.add('fade-in-up');
    });

    /* ---- Sticky navbar: elevate smoothly on scroll ---- */
    var navbar = document.querySelector('.site-navbar');
    if (navbar) {
        var onNavScroll = function () {
            navbar.classList.toggle('navbar-scrolled', window.scrollY > 8);
        };
        onNavScroll();
        window.addEventListener('scroll', onNavScroll, { passive: true });
    }

    /* ---- Hero product carousel ---- */
    document.querySelectorAll('[data-slider]').forEach(function (slider) {
        var track = slider.querySelector('[data-slider-track]');
        var prevBtn = slider.querySelector('[data-slider-prev]');
        var nextBtn = slider.querySelector('[data-slider-next]');
        if (!track) { return; }

        var stepSize = function () {
            var card = track.querySelector('.hero-slide');
            var gap = parseInt(getComputedStyle(track).gap, 10) || 16;
            return card ? card.offsetWidth + gap : track.clientWidth;
        };
        var atStart = function () { return track.scrollLeft <= 2; };
        var atEnd = function () {
            return track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
        };
        var refresh = function () {
            if (prevBtn) { prevBtn.disabled = atStart(); }
            if (nextBtn) { nextBtn.disabled = atEnd(); }
        };
        var move = function (dir) {
            track.scrollBy({ left: dir * stepSize(), behavior: 'smooth' });
        };

        if (prevBtn) { prevBtn.addEventListener('click', function () { move(-1); }); }
        if (nextBtn) { nextBtn.addEventListener('click', function () { move(1); }); }
        track.addEventListener('scroll', refresh, { passive: true });
        window.addEventListener('resize', refresh);
        refresh();

        // Gentle auto-advance; pauses while the user interacts with it
        var timer = null;
        var stop = function () {
            if (timer) { clearInterval(timer); timer = null; }
        };
        var play = function () {
            stop();
            if (track.scrollWidth <= track.clientWidth + 4) { return; }
            timer = setInterval(function () {
                if (atEnd()) {
                    track.scrollTo({ left: 0, behavior: 'smooth' });
                } else {
                    move(1);
                }
            }, 3800);
        };
        slider.addEventListener('mouseenter', stop);
        slider.addEventListener('mouseleave', play);
        slider.addEventListener('touchstart', stop, { passive: true });
        play();
    });
});
