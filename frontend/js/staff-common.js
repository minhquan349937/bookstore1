/**
 * Staff Common Utilities
 * Kiểm tra quyền staff, quản lý session
 */

// Kiểm tra staff authentication
function checkStaffAuth() {
    const staffToken = localStorage.getItem('staffToken');
    if (!staffToken) {
        window.location.href = '/staff/staff_login.html';
    }
}

// Logout staff
function staffLogout() {
    localStorage.removeItem('staffToken');
    window.location.href = '/staff/staff_login.html';
}

// Format currency VND
function formatPrice(price) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(price);
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) return;
    
    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    alertContainer.innerHTML = alertHTML;
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) alert.remove();
    }, 5000);
}

// Export functions
window.staffLogout = staffLogout;
window.formatPrice = formatPrice;
window.showAlert = showAlert;
window.checkStaffAuth = checkStaffAuth;
