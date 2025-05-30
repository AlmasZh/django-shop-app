// Improved Moderation Script with Better UX
document.addEventListener('DOMContentLoaded', function() {
    // Modal Elements
    const applicationModal = document.getElementById('application-modal');
    const closeModalButton = document.getElementById('close-modal');
    const modalContent = document.getElementById('modal-content');
    const modalActions = document.getElementById('modal-actions');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Sample Applications Data
    const applications = [
        {
            id: 1,
            name: "Aubakir Dias",
            email: "dias.aubakirov6@gmail.com",
            phone: "+87478301987",
            description: "I sell handmade crafts and artisanal goods. My store focuses on sustainable materials and traditional techniques.",
            date: "2025-03-10",
            status: "rejected",
        },
        // ... other application objects ...
    ];

    // Show application details with animation
    function showApplicationDetails(id) {
        const application = applications.find(app => app.id === parseInt(id));
        if (!application) return;
        
        // Show loading overlay
        showLoading();
        
        // Simulate API call delay
        setTimeout(() => {
            const initials = application.name.split(' ').map(n => n[0]).join('');
            const statusBadgeClass = getStatusBadgeClass(application.status);
            
            modalContent.innerHTML = `
                <div class="flex flex-col items-center gap-2 mb-4 animate-fade-in">
                    <div class="w-16 h-16 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xl font-medium shadow-inner">
                        ${initials}
                    </div>
                    <h3 class="text-xl font-semibold text-gray-800">${application.name}</h3>
                    <span class="px-3 py-1 text-xs font-medium rounded-full ${statusBadgeClass} shadow-sm">
                        ${application.status.charAt(0).toUpperCase() + application.status.slice(1)}
                    </span>
                </div>

                <div class="space-y-4 animate-fade-in-up">
                    <div>
                        <label class="text-sm font-medium text-gray-500">Email</label>
                        <div class="p-2 bg-gray-50 rounded-md text-gray-700 mt-1">${application.email}</div>
                    </div>
                    
                    <div>
                        <label class="text-sm font-medium text-gray-500">Phone</label>
                        <div class="p-2 bg-gray-50 rounded-md text-gray-700 mt-1">${application.phone}</div>
                    </div>
                    
                    <div>
                        <label class="text-sm font-medium text-gray-500">Store Description</label>
                        <div class="p-2 bg-gray-50 rounded-md text-gray-700 mt-1 whitespace-pre-wrap">
                            ${application.description}
                        </div>
                    </div>
                </div>
            `;
            
            if (application.status === 'pending') {
                modalActions.innerHTML = `
                    <button class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors w-full sm:w-auto reject-modal" data-id="${application.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                        Reject
                    </button>
                    <button class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors w-full sm:w-auto approve-modal" data-id="${application.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                        Approve
                    </button>
                `;
                
                // Add event listeners to modal buttons
                document.querySelector('.approve-modal').addEventListener('click', function() {
                    const id = this.getAttribute('data-id');
                    processApplication(id, 'approve');
                });
                
                document.querySelector('.reject-modal').addEventListener('click', function() {
                    const id = this.getAttribute('data-id');
                    processApplication(id, 'reject');
                });
            } else {
                modalActions.innerHTML = `
                    <button class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors w-full" id="close-modal-btn">
                        Close
                    </button>
                `;
                
                document.getElementById('close-modal-btn').addEventListener('click', closeModal);
            }
            
            hideLoading();
            openModal();
        }, 500); // Simulated delay
    }

    // Process application (approve/reject)
    function processApplication(id, action) {
        showLoading();
        
        // Simulate API call
        setTimeout(() => {
            if (action === 'approve') {
                approveApplication(id);
            } else {
                rejectApplication(id);
            }
            
            hideLoading();
            closeModal();
            
            // Show success notification
            showNotification(`Application ${action === 'approve' ? 'approved' : 'rejected'} successfully!`);
        }, 800);
    }

    // Show notification
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-md shadow-lg animate-fade-in-up';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('animate-fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Loading state functions
    function showLoading() {
        loadingOverlay.classList.remove('hidden');
        setTimeout(() => loadingOverlay.classList.add('opacity-100'), 10);
    }
    
    function hideLoading() {
        loadingOverlay.classList.remove('opacity-100');
        setTimeout(() => loadingOverlay.classList.add('hidden'), 300);
    }

    // Modal functions
    function openModal() {
        applicationModal.classList.remove('hidden');
        setTimeout(() => applicationModal.classList.add('opacity-100'), 10);
    }
    
    function closeModal() {
        applicationModal.classList.remove('opacity-100');
        setTimeout(() => applicationModal.classList.add('hidden'), 300);
    }

    // Helper functions
    function getStatusBadgeClass(status) {
        return {
            'approved': 'bg-green-100 text-green-800',
            'rejected': 'bg-red-100 text-red-800',
            'pending': 'bg-yellow-100 text-yellow-800'
        }[status] || 'bg-gray-100 text-gray-800';
    }

    // Event Listeners
    closeModalButton.addEventListener('click', closeModal);
    
    applicationModal.addEventListener('click', (e) => {
        if (e.target === applicationModal) {
            closeModal();
        }
    });

    // Add event delegation for dynamic elements
    document.addEventListener('click', function(e) {
        if (e.target.closest('.view-application')) {
            const id = e.target.closest('.view-application').getAttribute('data-id');
            showApplicationDetails(id);
        }
        
        if (e.target.closest('.approve-application')) {
            const id = e.target.closest('.approve-application').getAttribute('data-id');
            processApplication(id, 'approve');
        }
        
        if (e.target.closest('.reject-application')) {
            const id = e.target.closest('.reject-application').getAttribute('data-id');
            processApplication(id, 'reject');
        }
    });

    // Initialize animations
    function initAnimations() {
        // Add animation classes to elements
        const cards = document.querySelectorAll('.application-card');
        cards.forEach((card, index) => {
            card.classList.add('animate-fade-in-up');
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }
    
    initAnimations();
});

// Improved Cart Functionality
function setupCart() {
    // Format price with currency
    function formatPrice(price) {
        return new Intl.NumberFormat('ru-RU').format(price) + ' ₸';
    }

    // Quantity controls with animation
    document.querySelectorAll('.quantity-control').forEach(control => {
        control.addEventListener('click', function() {
            const itemElement = this.closest('.cart-item');
            const isIncrease = this.classList.contains('increase-quantity');
            const quantityElement = itemElement.querySelector('.item-quantity');
            let quantity = parseInt(quantityElement.textContent);
            
            // Add click animation
            this.classList.add('animate-pulse');
            setTimeout(() => this.classList.remove('animate-pulse'), 200);
            
            if (isIncrease) {
                quantity++;
            } else if (quantity > 1) {
                quantity--;
            }
            
            quantityElement.textContent = quantity;
            updateItemPrice(itemElement);
            updateTotals();
        });
    });

    // Remove item with confirmation
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', function() {
            const itemElement = this.closest('.cart-item');
            
            // Add removal animation
            itemElement.classList.add('animate-fade-out');
            
            setTimeout(() => {
                itemElement.remove();
                updateItemsCount();
                updateTotals();
                
                // Show undo notification if needed
                if (document.querySelectorAll('.cart-item').length === 0) {
                    showEmptyCartMessage();
                }
            }, 300);
        });
    });

    // Show empty cart message
    function showEmptyCartMessage() {
        const cartContainer = document.getElementById('cart-container');
        const emptyMessage = document.createElement('div');
        emptyMessage.className = 'text-center py-12 animate-fade-in';
        emptyMessage.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">Your cart is empty</h3>
            <p class="mt-1 text-gray-500">Start adding some items to your cart</p>
            <a href="/products" class="mt-6 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Continue Shopping
            </a>
        `;
        
        cartContainer.appendChild(emptyMessage);
    }

    // Initialize cart
    updateItemsCount();
    updateTotals();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('cart-container')) {
        setupCart();
    }
});