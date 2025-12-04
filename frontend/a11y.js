/**
 * Accessibility Utilities - Smart Hiring System
 * Helper functions for keyboard navigation, focus management, and ARIA
 */

class AccessibilityManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupSkipLinks();
        this.setupKeyboardNavigation();
        this.setupFocusManagement();
        this.setupLiveRegions();
        this.setupReducedMotion();
    }

    // ===== SKIP LINKS =====
    setupSkipLinks() {
        if (!document.querySelector('.skip-link')) {
            const skipLink = document.createElement('a');
            skipLink.href = '#main-content';
            skipLink.className = 'skip-link';
            skipLink.textContent = 'Skip to main content';
            document.body.insertBefore(skipLink, document.body.firstChild);

            skipLink.addEventListener('click', (e) => {
                e.preventDefault();
                const main = document.getElementById('main-content') || document.querySelector('main');
                if (main) {
                    main.focus();
                    main.scrollIntoView();
                }
            });
        }
    }

    // ===== KEYBOARD NAVIGATION =====
    setupKeyboardNavigation() {
        // Global keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + / : Show keyboard shortcuts
            if ((e.ctrlKey || e.metaKey) && e.key === '/') {
                e.preventDefault();
                this.showKeyboardShortcuts();
            }

            // Escape: Close modals/dropdowns
            if (e.key === 'Escape') {
                this.closeOpenElements();
            }

            // Ctrl/Cmd + K : Focus search (if exists)
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('input[type="search"]');
                if (searchInput) {
                    searchInput.focus();
                }
            }
        });

        // Arrow key navigation for lists
        this.setupArrowKeyNavigation();
    }

    setupArrowKeyNavigation() {
        document.querySelectorAll('[role="menu"], [role="listbox"]').forEach(container => {
            const items = Array.from(container.querySelectorAll('[role="menuitem"], [role="option"]'));
            let currentIndex = 0;

            container.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    currentIndex = (currentIndex + 1) % items.length;
                    items[currentIndex].focus();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    currentIndex = (currentIndex - 1 + items.length) % items.length;
                    items[currentIndex].focus();
                } else if (e.key === 'Home') {
                    e.preventDefault();
                    currentIndex = 0;
                    items[0].focus();
                } else if (e.key === 'End') {
                    e.preventDefault();
                    currentIndex = items.length - 1;
                    items[items.length - 1].focus();
                }
            });
        });
    }

    // ===== FOCUS MANAGEMENT =====
    setupFocusManagement() {
        // Focus trap for modals
        document.addEventListener('DOMNodeInserted', (e) => {
            const modal = e.target;
            if (modal.classList && modal.classList.contains('modal')) {
                this.trapFocusInModal(modal);
            }
        });
    }

    trapFocusInModal(modal) {
        const focusableElements = modal.querySelectorAll(
            'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );

        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        // Store previously focused element
        const previouslyFocused = document.activeElement;

        // Focus first element
        firstElement.focus();

        modal.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey && document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                } else if (!e.shiftKey && document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        });

        // Restore focus when modal closes
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (!document.contains(modal)) {
                    previouslyFocused.focus();
                    observer.disconnect();
                }
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    closeOpenElements() {
        // Close modals
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
            modal.setAttribute('aria-hidden', 'true');
        });

        // Close dropdowns
        document.querySelectorAll('[aria-expanded="true"]').forEach(el => {
            el.setAttribute('aria-expanded', 'false');
            const menuId = el.getAttribute('aria-controls');
            if (menuId) {
                const menu = document.getElementById(menuId);
                if (menu) menu.hidden = true;
            }
        });
    }

    // ===== LIVE REGIONS =====
    setupLiveRegions() {
        if (!document.querySelector('[aria-live]')) {
            // Create polite live region for announcements
            const liveRegion = document.createElement('div');
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.className = 'sr-only';
            liveRegion.id = 'live-region-polite';
            document.body.appendChild(liveRegion);

            // Create assertive live region for urgent announcements
            const assertiveRegion = document.createElement('div');
            assertiveRegion.setAttribute('aria-live', 'assertive');
            assertiveRegion.setAttribute('aria-atomic', 'true');
            assertiveRegion.className = 'sr-only';
            assertiveRegion.id = 'live-region-assertive';
            document.body.appendChild(assertiveRegion);
        }
    }

    announce(message, priority = 'polite') {
        const regionId = priority === 'assertive' ? 'live-region-assertive' : 'live-region-polite';
        const liveRegion = document.getElementById(regionId);
        
        if (liveRegion) {
            // Clear and set new message
            liveRegion.textContent = '';
            setTimeout(() => {
                liveRegion.textContent = message;
            }, 100);
        }
    }

    // ===== REDUCED MOTION =====
    setupReducedMotion() {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        if (prefersReducedMotion.matches) {
            document.documentElement.classList.add('reduce-motion');
        }

        prefersReducedMotion.addEventListener('change', (e) => {
            if (e.matches) {
                document.documentElement.classList.add('reduce-motion');
            } else {
                document.documentElement.classList.remove('reduce-motion');
            }
        });
    }

    // ===== KEYBOARD SHORTCUTS HELP =====
    showKeyboardShortcuts() {
        const shortcuts = [
            { keys: 'Tab', description: 'Navigate to next element' },
            { keys: 'Shift + Tab', description: 'Navigate to previous element' },
            { keys: 'Enter / Space', description: 'Activate button or link' },
            { keys: 'Escape', description: 'Close modal or dropdown' },
            { keys: 'Ctrl/Cmd + /', description: 'Show this help' },
            { keys: 'Ctrl/Cmd + K', description: 'Focus search' },
            { keys: 'Arrow Keys', description: 'Navigate lists and menus' },
            { keys: 'Home / End', description: 'Jump to first/last item' }
        ];

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-labelledby', 'shortcuts-title');
        modal.setAttribute('aria-modal', 'true');

        modal.innerHTML = `
            <div class="modal-overlay" aria-hidden="true"></div>
            <div class="modal-content" style="max-width: 600px; padding: 2rem;">
                <h2 id="shortcuts-title" style="margin-bottom: 1rem;">⌨️ Keyboard Shortcuts</h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th style="text-align: left; padding: 0.75rem; border-bottom: 2px solid #e5e7eb;">Keys</th>
                            <th style="text-align: left; padding: 0.75rem; border-bottom: 2px solid #e5e7eb;">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${shortcuts.map(s => `
                            <tr>
                                <td style="padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">
                                    <kbd style="background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-family: monospace;">${s.keys}</kbd>
                                </td>
                                <td style="padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">${s.description}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                <button onclick="this.closest('.modal').remove()" style="margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: #4F46E5; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    Close
                </button>
            </div>
        `;

        document.body.appendChild(modal);
        this.trapFocusInModal(modal);

        // Close on overlay click
        modal.querySelector('.modal-overlay').addEventListener('click', () => modal.remove());
    }

    // ===== FORM VALIDATION ANNOUNCEMENTS =====
    announceFormError(fieldName, error) {
        this.announce(`Error in ${fieldName}: ${error}`, 'assertive');
    }

    announceFormSuccess(message) {
        this.announce(message, 'polite');
    }

    // ===== LOADING STATE ANNOUNCEMENTS =====
    announceLoadingStart(message = 'Loading...') {
        this.announce(message, 'polite');
    }

    announceLoadingComplete(message = 'Content loaded') {
        this.announce(message, 'polite');
    }

    // ===== ARIA HELPERS =====
    setAriaExpanded(element, expanded) {
        element.setAttribute('aria-expanded', expanded.toString());
    }

    setAriaHidden(element, hidden) {
        element.setAttribute('aria-hidden', hidden.toString());
    }

    setAriaInvalid(element, invalid) {
        element.setAttribute('aria-invalid', invalid.toString());
    }

    setAriaDescribedBy(element, describedById) {
        element.setAttribute('aria-describedby', describedById);
    }

    // ===== FOCUS UTILITIES =====
    focusFirstError() {
        const firstError = document.querySelector('[aria-invalid="true"]');
        if (firstError) {
            firstError.focus();
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    setFocusTo(selector) {
        const element = typeof selector === 'string' ? document.querySelector(selector) : selector;
        if (element) {
            element.focus();
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

// Initialize accessibility manager
const a11y = new AccessibilityManager();

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.a11y = a11y;
}

// Announce page navigation (for SPAs)
window.addEventListener('popstate', () => {
    const title = document.title;
    a11y.announce(`Navigated to ${title}`, 'polite');
});

// Announce dynamic content changes
const contentObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            // Check if significant content was added
            const hasSignificantContent = Array.from(mutation.addedNodes).some(node => {
                return node.nodeType === Node.ELEMENT_NODE && 
                       node.textContent.trim().length > 50;
            });

            if (hasSignificantContent) {
                // Optional: announce content changes
                // a11y.announce('New content loaded', 'polite');
            }
        }
    });
});

// Observe main content area for changes
const mainContent = document.getElementById('main-content') || document.querySelector('main');
if (mainContent) {
    contentObserver.observe(mainContent, { childList: true, subtree: true });
}
