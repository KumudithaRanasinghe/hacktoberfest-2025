// Main JavaScript for Hacktoberfest 2025 Project Tracker

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers
    initializeBootstrapComponents();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Initialize theme handling
    initializeTheme();
    
    // Add loading states to forms
    addFormLoadingStates();
    
    // Initialize auto-refresh for dashboard
    initializeAutoRefresh();
});

/**
 * Initialize Bootstrap components
 */
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Add smooth scrolling to anchor links
 */
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize theme handling
 */
function initializeTheme() {
    // Check for saved theme preference or default to system preference
    const savedTheme = localStorage.getItem('theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const theme = savedTheme || systemTheme;
    
    setTheme(theme);
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

/**
 * Set the theme
 */
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

/**
 * Add loading states to forms
 */
function addFormLoadingStates() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                form.classList.add('loading');
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Submit';
                    form.classList.remove('loading');
                }, 10000);
            }
        });
    });
}

/**
 * Initialize auto-refresh for dashboard
 */
function initializeAutoRefresh() {
    if (window.location.pathname === '/') {
        // Refresh statistics every 5 minutes
        setInterval(refreshDashboardStats, 300000);
    }
}

/**
 * Refresh dashboard statistics
 */
async function refreshDashboardStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        // Update stat cards
        updateStatCard('total-contributors', stats.total_contributors);
        updateStatCard('total-contributions', stats.total_contributions);
        updateStatCard('unique-repositories', stats.unique_repositories);
        updateStatCard('avg-contributions', stats.avg_contributions_per_contributor.toFixed(1));
        
        console.log('Dashboard stats refreshed');
    } catch (error) {
        console.error('Error refreshing dashboard stats:', error);
    }
}

/**
 * Update a stat card value
 */
function updateStatCard(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
        element.classList.add('fade-in');
        setTimeout(() => element.classList.remove('fade-in'), 500);
    }
}

/**
 * Utility function to format dates
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Utility function to format relative time
 */
function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
    } else {
        const months = Math.floor(diffDays / 30);
        return `${months} month${months > 1 ? 's' : ''} ago`;
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success');
    } catch (err) {
        console.error('Failed to copy: ', err);
        showNotification('Failed to copy to clipboard', 'error');
    }
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Get contribution type badge color
 */
function getContributionTypeColor(type) {
    const colors = {
        'bug-fix': 'danger',
        'feature': 'success',
        'documentation': 'info',
        'testing': 'warning',
        'refactoring': 'purple',
        'enhancement': 'orange'
    };
    return colors[type] || 'secondary';
}

/**
 * Format contribution type for display
 */
function formatContributionType(type) {
    return type.split('-').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

/**
 * Animate counter
 */
function animateCounter(element, target, duration = 1000) {
    const start = parseInt(element.textContent) || 0;
    const increment = (target - start) / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        element.textContent = Math.round(current);
        
        if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
            element.textContent = target;
            clearInterval(timer);
        }
    }, 16);
}

/**
 * Initialize search functionality
 */
function initializeSearch(inputSelector, itemSelector, searchKey) {
    const searchInput = document.querySelector(inputSelector);
    if (!searchInput) return;
    
    const debouncedSearch = debounce((searchTerm) => {
        const items = document.querySelectorAll(itemSelector);
        
        items.forEach(item => {
            const searchText = item.getAttribute(searchKey) || item.textContent;
            if (searchText.toLowerCase().includes(searchTerm.toLowerCase())) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }, 300);
    
    searchInput.addEventListener('input', (e) => {
        debouncedSearch(e.target.value);
    });
}

/**
 * Initialize sorting functionality
 */
function initializeSort(selectSelector, itemSelector, containerSelector) {
    const sortSelect = document.querySelector(selectSelector);
    if (!sortSelect) return;
    
    sortSelect.addEventListener('change', (e) => {
        const sortBy = e.target.value;
        const container = document.querySelector(containerSelector);
        const items = Array.from(container.querySelectorAll(itemSelector));
        
        items.sort((a, b) => {
            const aValue = a.getAttribute(`data-${sortBy}`) || a.textContent;
            const bValue = b.getAttribute(`data-${sortBy}`) || b.textContent;
            
            if (sortBy === 'contributions' || sortBy === 'date') {
                return parseInt(bValue) - parseInt(aValue); // Descending
            } else {
                return aValue.localeCompare(bValue); // Ascending
            }
        });
        
        // Clear container and re-append sorted items
        container.innerHTML = '';
        items.forEach(item => container.appendChild(item));
    });
}

/**
 * Export data as JSON
 */
async function exportData(endpoint, filename) {
    try {
        const response = await fetch(endpoint);
        const data = await response.json();
        
        const blob = new Blob([JSON.stringify(data, null, 2)], {
            type: 'application/json'
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('Data exported successfully!', 'success');
    } catch (error) {
        console.error('Export failed:', error);
        showNotification('Export failed. Please try again.', 'danger');
    }
}

// Global utility functions
window.HacktoberfestUI = {
    showNotification,
    copyToClipboard,
    formatDate,
    formatRelativeTime,
    getContributionTypeColor,
    formatContributionType,
    animateCounter,
    exportData
};
