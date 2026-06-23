// About section functionality
class AboutSection {
    constructor() {
        this.features = [
            {
                iconClass: "fas fa-heart",
                title: "Loving Community",
                description: "A welcoming family where everyone belongs and grows together in faith."
            },
            {
                iconClass: "fas fa-book",
                title: "Biblical Teaching",
                description: "Grounded in Scripture with practical application for daily living and spiritual growth."
            },
            {
                iconClass: "fas fa-users",
                title: "Active Ministry",
                description: "Engaging ministries for all ages, especially our vibrant youth community."
            }
        ];
        this.init();
    }

    createFeatureCard(feature) {
        return `
            <div class="card p-6 hover-shadow-gentle transition-all duration-300 hover-scale-105">
                <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0">
                        <i class="${feature.iconClass} w-8 h-8 text-warm-gold"></i>
                    </div>
                    <div>
                        <h4 class="text-lg font-semibold text-spiritual mb-2">
                            ${feature.title}
                        </h4>
                        <p class="text-muted-foreground">
                            ${feature.description}
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    init() {
        const aboutSection = document.getElementById('about');
        if (!aboutSection) return;

        // Render features
        const featuresContainer = aboutSection.querySelector('.features-grid');
        if (featuresContainer) {
            featuresContainer.innerHTML = this.features
                .map(feature => this.createFeatureCard(feature))
                .join('');
        }

        // Add animation on scroll
        const cards = aboutSection.querySelectorAll('.card');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, { threshold: 0.1 });

        cards.forEach(card => observer.observe(card));
    }

    static init() {
        new AboutSection();
    }
}

// Initialize about section on page load
document.addEventListener('DOMContentLoaded', AboutSection.init);document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contactForm');
    if (!form) return;
    
    const formStatus = form.querySelector('.form-status');

    // Error messages for validation
    const errorMessages = {
        firstName: {
            valueMissing: 'Please enter your first name',
            patternMismatch: 'Please use only letters in your first name',
            tooShort: 'First name must be at least 2 characters long'
        },
        lastName: {
            valueMissing: 'Please enter your last name',
            patternMismatch: 'Please use only letters in your last name',
            tooShort: 'Last name must be at least 2 characters long'
        },
        email: {
            valueMissing: 'Please enter your email address',
            typeMismatch: 'Please enter a valid email address'
        },
        subject: {
            valueMissing: 'Please select a subject'
        },
        message: {
            valueMissing: 'Please enter your message',
            tooShort: 'Message must be at least 10 characters long'
        }
    };

    // Show appropriate error message for each field
    const showError = (input) => {
        const errorElement = document.getElementById(`${input.id}-error`);
        if (!errorElement) return;

        let message = '';
        const messages = errorMessages[input.id];

        if (input.validity.valueMissing && messages.valueMissing) {
            message = messages.valueMissing;
        } else if (input.validity.typeMismatch && messages.typeMismatch) {
            message = messages.typeMismatch;
        } else if (input.validity.patternMismatch && messages.patternMismatch) {
            message = messages.patternMismatch;
        } else if (input.validity.tooShort && messages.tooShort) {
            message = messages.tooShort;
        }

        errorElement.textContent = message;
    };

    // Validate a single field
    const validateField = (input) => {
        if (input.validity.valid) {
            document.getElementById(`${input.id}-error`).textContent = '';
        } else {
            showError(input);
        }
    };

    // Add validation listeners to all form fields
    form.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => validateField(input));
    });

    // Form submission handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Check if the form is valid
        if (!form.checkValidity()) {
            // Show validation messages
            form.querySelectorAll('input, select, textarea').forEach(input => {
                validateField(input);
            });
            return;
        }

        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.classList.add('loading');
        submitButton.disabled = true;

        try {
            // Collect form data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            // Send to Formspree (replace YOUR_FORM_ID with your actual Formspree form ID)
            // Sign up at https://formspree.io to get your form ID
            const response = await fetch('https://formspree.io/f/YOUR_FORM_ID', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                // Show success message
                formStatus.className = 'form-status success';
                formStatus.innerHTML = '<i class="fas fa-check-circle"></i> Thank you! Your message has been sent successfully. We will get back to you soon.';
                form.reset();

                // Hide success message after 8 seconds
                setTimeout(() => {
                    formStatus.className = 'form-status';
                    formStatus.innerHTML = '';
                }, 8000);
            } else {
                throw new Error('Form submission failed');
            }

        } catch (error) {
            // Show error message
            formStatus.className = 'form-status error';
            formStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> Sorry, there was a problem sending your message. Please try again or contact us directly at info@lavertransformation.org';
        } finally {
            // Remove loading state
            submitButton.classList.remove('loading');
            submitButton.disabled = false;
        }
    });
});// Image optimization
class ImageOptimizer {
    constructor() {
        if (ImageOptimizer.instance) {
            return ImageOptimizer.instance;
        }
        ImageOptimizer.instance = this;

        this.loadedImages = new Set();
        this.observer = new IntersectionObserver(
            this.handleIntersection.bind(this),
            {
                root: null,
                rootMargin: '50px',
                threshold: 0.1
            }
        );

        return this;
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.loadImage(entry.target);
                this.observer.unobserve(entry.target);
            }
        });
    }

    loadImage(img) {
        const src = img.dataset.src;
        if (!src || this.loadedImages.has(src)) return;

        // Load responsive image based on viewport width
        const viewportWidth = window.innerWidth;
        const srcset = img.dataset.srcset;

        if (srcset) {
            const sources = srcset.split(',').map(s => {
                const [url, width] = s.trim().split(' ');
                return {
                    url,
                    width: parseInt(width.replace('w', ''))
                };
            });

            // Find the best matching image size
            const bestMatch = sources.reduce((prev, curr) => {
                const prevDiff = Math.abs(prev.width - viewportWidth);
                const currDiff = Math.abs(curr.width - viewportWidth);
                return currDiff < prevDiff ? curr : prev;
            });

            img.src = bestMatch.url;
        } else {
            img.src = src;
        }

        img.onload = () => {
            img.classList.add('loaded');
            this.loadedImages.add(src);
        };
    }

    observe(img) {
        if (!img.dataset.src) return;
        this.observer.observe(img);
    }

    observeAll() {
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.observe(img);
        });
    }

    static getInstance() {
        if (!this.instance) {
            this.instance = new ImageOptimizer();
        }
        return this.instance;
    }
}

// Initialize lazy loading on page load
document.addEventListener('DOMContentLoaded', () => {
    const imageOptimizer = ImageOptimizer.getInstance();
    imageOptimizer.observeAll();

    // Rerun observation when new content is loaded dynamically
    const observer = new MutationObserver((mutations) => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node instanceof HTMLElement) {
                    node.querySelectorAll('img[data-src]').forEach(img => {
                        imageOptimizer.observe(img);
                    });
                }
            });
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});// Loading states
class LoadingState {
    constructor(element, loadingClass = 'loading', ariaLabel = 'Loading...') {
        this.element = element;
        this.loadingClass = loadingClass;
        this.ariaLabel = ariaLabel;
    }

    start() {
        this.element.classList.add(this.loadingClass);
        this.element.setAttribute('aria-busy', 'true');
        this.element.setAttribute('aria-label', this.ariaLabel);
    }

    stop() {
        this.element.classList.remove(this.loadingClass);
        this.element.removeAttribute('aria-busy');
        this.element.removeAttribute('aria-label');
    }
}

// Image gallery loading handler
class ImageGalleryLoader {
    constructor(galleryId) {
        const gallery = document.getElementById(galleryId);
        if (!gallery) {
            console.warn(`Gallery with id ${galleryId} not found`);
            return;
        }
        this.gallery = gallery;
        this.images = this.gallery.querySelectorAll('img');
        this.loadingState = new LoadingState(this.gallery, 'gallery-loading', 'Loading gallery images...');
        this.init();
    }

    init() {
        this.loadingState.start();
        let loadedImages = 0;

        const checkAllLoaded = () => {
            loadedImages++;
            if (loadedImages === this.images.length) {
                this.loadingState.stop();
            }
        };

        this.images.forEach(img => {
            if (img.complete) {
                checkAllLoaded();
            } else {
                img.addEventListener('load', checkAllLoaded);
                img.addEventListener('error', checkAllLoaded);
            }
        });
    }
}

// Sermon player loading handler
class SermonPlayerLoader {
    constructor(playerId) {
        const player = document.getElementById(playerId);
        if (!player) {
            console.warn(`Player with id ${playerId} not found`);
            return;
        }
        this.player = player;
        
        const audio = player.querySelector('audio');
        if (!audio) {
            console.warn(`Audio element not found in player ${playerId}`);
            return;
        }
        this.audio = audio;

        this.loadingState = new LoadingState(this.player, 'player-loading', 'Loading sermon audio...');
        this.init();
    }

    init() {
        this.audio.addEventListener('loadstart', () => {
            this.loadingState.start();
        });

        this.audio.addEventListener('canplay', () => {
            this.loadingState.stop();
        });

        this.audio.addEventListener('error', () => {
            this.loadingState.stop();
            this.player.classList.add('error');
        });
    }
}

// Initialize loading states
document.addEventListener('DOMContentLoaded', () => {
    // Initialize gallery loaders
    document.querySelectorAll('.gallery').forEach((gallery, index) => {
        gallery.id = gallery.id || `gallery-${index}`;
        new ImageGalleryLoader(gallery.id);
    });

    // Initialize sermon players
    document.querySelectorAll('.sermon-player').forEach((player, index) => {
        player.id = player.id || `sermon-player-${index}`;
        new SermonPlayerLoader(player.id);
    });
});// Mobile menu enhancements
class MobileMenu {
    constructor() {
        this.menu = document.querySelector('.nav-menu');
        this.toggle = document.querySelector('.mobile-menu');
        this.isOpen = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.SWIPE_THRESHOLD = 50;
        
        if (!this.menu || !this.toggle) {
            console.warn('Mobile menu elements not found');
            return;
        }

        this.createOverlay();
        this.init();
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'mobile-menu-overlay';
        document.body.appendChild(this.overlay);

        this.overlay.addEventListener('click', () => {
            this.close();
        });
    }

    init() {
        // Toggle button click handler
        this.toggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.isOpen ? this.close() : this.open();
        });

        // Touch event handlers
        this.menu.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
        });

        this.menu.addEventListener('touchmove', (e) => {
            if (!this.isOpen) return;

            const touchX = e.touches[0].clientX;
            const touchY = e.touches[0].clientY;
            
            // Calculate swipe distance and angle
            const deltaX = touchX - this.touchStartX;
            const deltaY = touchY - this.touchStartY;
            const angle = Math.abs(Math.atan2(deltaY, deltaX) * 180 / Math.PI);

            // Only handle horizontal swipes (angle less than 45 degrees)
            if (angle < 45) {
                e.preventDefault();
                if (deltaX < 0) {
                    this.menu.style.transform = `translateX(${deltaX}px)`;
                }
            }
        });

        this.menu.addEventListener('touchend', (e) => {
            if (!this.isOpen) return;

            const touchX = e.changedTouches[0].clientX;
            const deltaX = touchX - this.touchStartX;

            if (Math.abs(deltaX) > this.SWIPE_THRESHOLD) {
                if (deltaX < 0) {
                    this.close();
                }
            } else {
                this.menu.style.transform = '';
            }
        });

        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Close menu on resize if in desktop view
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && this.isOpen) {
                this.close();
            }
        });
    }

    open() {
        this.isOpen = true;
        this.menu.classList.add('active');
        this.toggle.classList.add('active');
        this.overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Animate menu items
        this.menu.querySelectorAll('.nav-item').forEach((item, index) => {
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, 100 * index);
        });
    }

    close() {
        this.isOpen = false;
        this.menu.style.transform = '';
        this.menu.classList.remove('active');
        this.toggle.classList.remove('active');
        this.overlay.classList.remove('active');
        document.body.style.overflow = '';

        // Reset menu items
        this.menu.querySelectorAll('.nav-item').forEach(item => {
            item.style.opacity = '';
            item.style.transform = '';
        });
    }
}

// Initialize mobile menu on page load
document.addEventListener('DOMContentLoaded', () => {
    new MobileMenu();
});// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('.nav-container');
    const mobileMenuBtn = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    const navButtons = document.querySelector('.nav-buttons');
    const scrollProgress = document.querySelector('.scroll-progress');
    const links = document.querySelectorAll('.nav-links a');

    // Handle scroll effects
    window.addEventListener('scroll', () => {
        // Add/remove scrolled class
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }

        // Update scroll progress
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        scrollProgress.style.width = scrolled + '%';
    });

    // Mobile menu toggle
    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        navButtons.classList.toggle('active');
    });

    // Active link highlighting
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.scrollY >= (sectionTop - 300)) {
                current = section.getAttribute('id');
            }
        });

        links.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').slice(1) === current) {
                link.classList.add('active');
            }
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!nav.contains(e.target) && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            navButtons.classList.remove('active');
        }
    });
});// Social sharing functionality
class SocialShare {
    constructor(container, title, description = '') {
        this.SHARE_APIS = {
            facebook: (url, title) => 
                `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
            twitter: (url, title) => 
                `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
            whatsapp: (url, title) => 
                `https://wa.me/?text=${encodeURIComponent(`${title} ${url}`)}`,
            email: (url, title) => 
                `mailto:?subject=${encodeURIComponent(title)}&body=${encodeURIComponent(`Check this out: ${url}`)}`,
            linkedin: (url, title) => 
                `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`
        };

        this.container = container;
        this.title = title;
        this.description = description;
        this.url = window.location.href;
        this.init();
    }

    init() {
        // Create share buttons container
        const shareButtonsContainer = document.createElement('div');
        shareButtonsContainer.className = 'share-buttons';
        
        // Add share heading
        const heading = document.createElement('h4');
        heading.className = 'share-heading';
        heading.textContent = 'Share This';
        shareButtonsContainer.appendChild(heading);

        // Add share buttons
        Object.keys(this.SHARE_APIS).forEach(platform => {
            const button = this.createShareButton(platform);
            shareButtonsContainer.appendChild(button);
        });

        // Add native share button if available
        if ('share' in navigator) {
            const nativeButton = this.createNativeShareButton();
            shareButtonsContainer.appendChild(nativeButton);
        }

        this.container.appendChild(shareButtonsContainer);
    }

    createShareButton(platform) {
        const button = document.createElement('button');
        button.className = `share-button share-${platform}`;
        button.setAttribute('aria-label', `Share on ${platform}`);

        const icon = document.createElement('i');
        icon.className = platform === 'email' ? 'fas fa-envelope' : `fab fa-${platform}`;
        button.appendChild(icon);

        button.addEventListener('click', (e) => {
            e.preventDefault();
            const shareUrl = this.SHARE_APIS[platform](this.url, this.title);
            window.open(shareUrl, '_blank', 'width=600,height=400');
        });

        return button;
    }

    createNativeShareButton() {
        const button = document.createElement('button');
        button.className = 'share-button share-native';
        button.setAttribute('aria-label', 'Share');

        const icon = document.createElement('i');
        icon.className = 'fas fa-share-alt';
        button.appendChild(icon);

        button.addEventListener('click', async () => {
            try {
                await navigator.share({
                    title: this.title,
                    text: this.description,
                    url: this.url
                });
            } catch (err) {
                console.log('Error sharing:', err);
            }
        });

        return button;
    }

    static init() {
        // Initialize share buttons for all sharable content
        document.querySelectorAll('[data-sharable]').forEach(element => {
            const title = element.getAttribute('data-share-title') || document.title;
            const description = element.getAttribute('data-share-description') || '';
            new SocialShare(element, title, description);
        });
    }
}

// Initialize social sharing on page load
document.addEventListener('DOMContentLoaded', () => {
    SocialShare.init();
});