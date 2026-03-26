/**
 * Common API & Utilities
 * Xử lý token, API calls, localStorage
 */

const API_BASE = 'http://localhost:8000/api';
const BOOK_API = 'http://localhost:8001/api';
const LAPTOP_API = 'http://localhost:8006/api';
const MOBILE_API = 'http://localhost:8007/api';
const CUSTOMER_API = 'http://localhost:8002/api';

// ============ TOKEN MANAGEMENT ============
class AuthManager {
    static getToken() {
        return localStorage.getItem('authToken');
    }

    static setToken(token) {
        localStorage.setItem('authToken', token);
    }

    static removeToken() {
        localStorage.removeItem('authToken');
    }

    static getCustomerId() {
        return localStorage.getItem('customerId');
    }

    static setCustomerId(id) {
        localStorage.setItem('customerId', id);
    }

    static isLoggedIn() {
        return !!this.getToken();
    }

    static getCurrentUser() {
        const user = localStorage.getItem('currentUser');
        return user ? JSON.parse(user) : null;
    }

    static setCurrentUser(userData) {
        localStorage.setItem('currentUser', JSON.stringify(userData));
    }

    static logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('customerId');
        localStorage.removeItem('currentUser');
        window.location.href = '/login.html';
    }
}

// ============ API CALLS ============
class API {
    static async call(method, endpoint, data = null) {
        const url = endpoint.startsWith('http') ? endpoint : CUSTOMER_API + endpoint;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        // Only send token to Customer Service endpoints, not to other microservices
        const isCrossService = endpoint.startsWith('http');
        const token = AuthManager.getToken();
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

    // USER ENDPOINTS
    static async register(email, password, username, phone = '', address = '') {
        return this.call('POST', '/users/register/', {
            email,
            password,
            username,
            phone,
            address
        });
    }

    static async login(username, password) {
        return this.call('POST', '/users/login/', {
            username,
            password
        });
    }

    static async getProfile() {
        return this.call('GET', '/users/profile/');
    }

    // BOOK ENDPOINTS (Book Service - Port 8001)
    static async getBooks(page = 1, limit = 12) {
        const bookApi = 'http://localhost:8001/api';
        return this.call('GET', `${bookApi}/books/?page=${page}&limit=${limit}`);
    }

    static async searchBooks(query, sort = 'newest', page = 1) {
        const bookApi = 'http://localhost:8001/api';
        return this.call('GET', `${bookApi}/books/search/?q=${query}&sort=${sort}&page=${page}`);
    }

    static async getBookById(bookId) {
        const bookApi = 'http://localhost:8001/api';
        return this.call('GET', `${bookApi}/books/${bookId}/`);
    }

    // CART ENDPOINTS (Cart Service - Port 8005)
    static async addToCart(customerId, bookId, quantity = 1, price = 0) {
        const cartApi = 'http://localhost:8005/api';
        return this.call('POST', `${cartApi}/carts/${customerId}/add_item/`, {
            book_id: bookId,
            quantity,
            price
        });
    }

    static async getCart(customerId) {
        const cartApi = 'http://localhost:8005/api';
        return this.call('GET', `${cartApi}/carts/${customerId}/`);
    }

    static async removeFromCart(customerId, bookId) {
        const cartApi = 'http://localhost:8005/api';
        return this.call('POST', `${cartApi}/carts/${customerId}/remove_item/`, {
            book_id: bookId
        });
    }

    static async updateCartQuantity(customerId, bookId, quantity) {
        const cartApi = 'http://localhost:8005/api';
        return this.call('POST', `${cartApi}/carts/${customerId}/update_quantity/`, {
            book_id: bookId,
            quantity
        });
    }

    static async clearCart(customerId) {
        const cartApi = 'http://localhost:8005/api';
        return this.call('POST', `${cartApi}/carts/${customerId}/clear/`);
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

function checkAuth() {
    if (!AuthManager.isLoggedIn()) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

function getQueryParam(param) {
    const params = new URLSearchParams(window.location.search);
    return params.get(param);
}

function navigateToDetail(bookId) {
    window.location.href = `/detail.html?id=${bookId}`;
}

// ============ UPDATE NAVBAR ============
function updateNavbar() {
    const user = AuthManager.getCurrentUser();
    const navbarRight = document.getElementById('navbarRight');
    
    if (navbarRight) {
        if (AuthManager.isLoggedIn() && user) {
            navbarRight.innerHTML = `
                <div class="d-flex align-items-center gap-3">
                    <span class="text-muted">Xin chào, <strong>${user.username}</strong></span>
                    <button class="btn btn-sm btn-outline-danger" onclick="AuthManager.logout()">
                        Đăng xuất
                    </button>
                </div>
            `;
        } else {
            navbarRight.innerHTML = `
                <div class="gap-2 d-flex">
                    <a href="/login.html" class="btn btn-sm btn-outline-primary">Đăng nhập</a>
                    <a href="/register.html" class="btn btn-sm btn-primary">Đăng ký</a>
                </div>
            `;
        }
    }
}

// ============ INIT ON PAGE LOAD ============
document.addEventListener('DOMContentLoaded', () => {
    updateNavbar();
});
