/**
 * Staff API & Utilities
 * Xử lý authentication của nhân viên
 */

const STAFF_API = 'http://localhost:8003/api';
const BOOK_API = 'http://localhost:8001/api';

// ============ STAFF AUTH ============
class StaffAuthManager {
    static getToken() {
        return localStorage.getItem('staffToken');
    }

    static setToken(token) {
        localStorage.setItem('staffToken', token);
    }

    static removeToken() {
        localStorage.removeItem('staffToken');
    }

    static getStaffId() {
        return localStorage.getItem('staffId');
    }

    static setStaffId(id) {
        localStorage.setItem('staffId', id);
    }

    static getCurrentStaff() {
        const staff = localStorage.getItem('currentStaff');
        return staff ? JSON.parse(staff) : null;
    }

    static setCurrentStaff(staffData) {
        localStorage.setItem('currentStaff', JSON.stringify(staffData));
    }

    static isLoggedIn() {
        return !!this.getToken();
    }

    static logout() {
        localStorage.removeItem('staffToken');
        localStorage.removeItem('staffId');
        localStorage.removeItem('currentStaff');
        window.location.href = '/staff/staff_login.html';
    }
}

// ============ STAFF API CALLS ============
class StaffAPI {
    static async call(method, endpoint, data = null) {
        const url = endpoint.startsWith('http') ? endpoint : STAFF_API + endpoint;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        // Only send token to Staff Service endpoints, not to other microservices
        const isCrossService = endpoint.startsWith('http');
        const token = StaffAuthManager.getToken();
        if (token && !isCrossService) {
            options.headers['Authorization'] = `Token ${token}`;
        }

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || result.error || 'API Error');
            }

            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // STAFF LOGIN
    static async staffLogin(username, password) {
        return this.call('POST', '/staff-users/login/', {
            username,
            password
        });
    }

    // BOOK OPERATIONS
    static async getBooks(page = 1, limit = 20) {
        return this.call('GET', `${BOOK_API}/books/?page=${page}&limit=${limit}`);
    }

    static async getBookById(bookId) {
        return this.call('GET', `${BOOK_API}/books/${bookId}/`);
    }

    static async createBook(bookData) {
        return this.call('POST', `${BOOK_API}/books/`, bookData);
    }

    static async updateBook(bookId, bookData) {
        return this.call('PUT', `${BOOK_API}/books/${bookId}/`, bookData);
    }

    static async deleteBook(bookId) {
        return this.call('DELETE', `${BOOK_API}/books/${bookId}/`);
    }

    // STAFF BOOK MANAGEMENT (Through Staff Service)
    static async staffListBooks(page = 1) {
        return this.call('GET', '/staff-book-management/list_books/?page=' + page);
    }

    static async staffAddBook(bookData) {
        return this.call('POST', '/staff-book-management/add_book/', bookData);
    }

    static async staffEditBook(bookId, bookData) {
        return this.call('POST', '/staff-book-management/edit_book/', {
            book_id: bookId,
            ...bookData
        });
    }

    static async staffIncreaseStock(bookId, quantity) {
        return this.call('POST', `${BOOK_API}/books/${bookId}/increase_stock/`, {
            quantity
        });
    }

    static async staffDecreaseStock(bookId, quantity) {
        return this.call('POST', `${BOOK_API}/books/${bookId}/decrease_stock/`, {
            quantity
        });
    }

    // STATS & REPORTS
    static async getStats() {
        return this.call('GET', `/staff-book-management/report/`);
    }
}

// ============ UTILITY FUNCTIONS ============
function formatPrice(price) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(price);
}

function showAlert(message, type = 'info') {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <strong>${type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ'}</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertContainer = document.getElementById('alertContainer');
    if (alertContainer) {
        alertContainer.innerHTML = alertHTML;
        setTimeout(() => {
            alertContainer.innerHTML = '';
        }, 3000);
    }
}

function checkStaffAuth() {
    if (!StaffAuthManager.isLoggedIn()) {
        window.location.href = '/staff/staff_login.html';
        return false;
    }
    return true;
}

function getQueryParam(param) {
    const params = new URLSearchParams(window.location.search);
    return params.get(param);
}

// ============ UPDATE STAFF NAVBAR ============
function updateStaffNavbar() {
    const staff = StaffAuthManager.getCurrentStaff();
    const navbarRight = document.getElementById('navbarRight');
    
    if (navbarRight) {
        if (StaffAuthManager.isLoggedIn() && staff) {
            navbarRight.innerHTML = `
                <div class="d-flex align-items-center gap-3">
                    <span class="text-muted">
                        👤 <strong>${staff.username}</strong>
                        <br>
                        <small class="text-muted">Quyền: ${staff.role || 'Chưa xác định'}</small>
                    </span>
                    <button class="btn btn-sm btn-outline-danger" onclick="StaffAuthManager.logout()">
                        Đăng xuất
                    </button>
                </div>
            `;
        }
    }
}

// ============ INIT ON PAGE LOAD ============
document.addEventListener('DOMContentLoaded', () => {
    updateStaffNavbar();
});
