// API Configuration
const API_CONFIG = {
    ITEMS_URL: 'http://items-service:5001',
    REVIEWS_URL: 'http://reviews-service:8081',
    WIREMOCK_URL: 'http://wiremock:8080'
};

// Get URLs from window location for browser-based requests
function getItemsServiceUrl() {
    return window.location.protocol + '//' + window.location.hostname + ':5001';
}

function getReviewsServiceUrl() {
    return window.location.protocol + '//' + window.location.hostname + ':8081';
}

function getWiremockUrl() {
    return window.location.protocol + '//' + window.location.hostname + ':8080';
}

/**
 * Fetch wrapper for API calls
 */
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        const data = await response.json();
        return { success: true, data, status: response.status };
    } catch (error) {
        console.error('Fetch error:', error);
        return { success: false, error: error.message, status: 0 };
    }
}

/**
 * Display message to user
 */
function showMessage(text, type = 'info') {
    const messageDiv = document.getElementById('message');
    if (!messageDiv) return;
    
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

/**
 * Display table
 */
function displayTable(data, columns, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (!data || data.length === 0) {
        container.innerHTML = '<p>No data available</p>';
        return;
    }
    
    let html = '<table><thead><tr>';
    columns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    data.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            const value = row[col] !== null && row[col] !== undefined ? row[col] : '-';
            html += `<td>${value}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

/**
 * Render form
 */
function renderForm(fields, onSubmit, formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    let html = '';
    fields.forEach(field => {
        html += `
            <div class="form-group">
                <label for="${field.id}">${field.label}</label>
                <input 
                    type="${field.type || 'text'}" 
                    id="${field.id}" 
                    name="${field.name}"
                    ${field.required ? 'required' : ''}
                    ${field.step ? `step="${field.step}"` : ''}
                />
            </div>
        `;
    });
    html += `<button type="submit" class="btn-primary">Submit</button>`;
    
    form.innerHTML = html;
    form.onsubmit = (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        onSubmit(data);
    };
}

/**
 * Parse datetime-local value
 */
function formatDatetimeLocal(value) {
    if (!value) return null;
    // datetime-local format: 2024-01-01T10:00
    return value.replace('T', ' ') + ':00';
}

/**
 * Get available providers information
 */
function getAvailableProviders() {
    return [
        {
            name: 'CMOT',
            description: 'Provider that returns error (test failure scenario)',
            shouldSucceed: false,
            status: 'FAILS'
        },
        {
            name: 'Throat',
            description: 'Provider that returns error (test failure scenario)',
            shouldSucceed: false,
            status: 'FAILS'
        },
        {
            name: 'AirlineA',
            description: 'Provider that returns success',
            shouldSucceed: true,
            status: 'SUCCESS'
        },
        {
            name: 'AirlineB',
            description: 'Provider that returns success',
            shouldSucceed: true,
            status: 'SUCCESS'
        },
        {
            name: 'AirlineC',
            description: 'Provider that returns success',
            shouldSucceed: true,
            status: 'SUCCESS'
        }
    ];
}

/**
 * Test a provider endpoint
 */
async function testProvider(providerName, items) {
    const startTime = performance.now();
    const url = `${getWiremockUrl()}/provider/${encodeURIComponent(providerName)}`;
    
    try {
        // Parse items if it's a string
        let parsedItems = items;
        if (typeof items === 'string') {
            parsedItems = JSON.parse(items);
        }
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(parsedItems)
        });
        
        const endTime = performance.now();
        const responseTime = (endTime - startTime).toFixed(2);
        
        const data = await response.json();
        
        return {
            success: response.ok,
            status: response.status,
            responseTime: responseTime,
            data: data,
            error: null
        };
    } catch (error) {
        const endTime = performance.now();
        const responseTime = (endTime - startTime).toFixed(2);
        
        console.error('Provider test error:', error);
        return {
            success: false,
            status: 0,
            responseTime: responseTime,
            data: null,
            error: error.message
        };
    }
}

/**
 * Get predefined test items
 */
function getPredefinedTestItems() {
    return [
        {
            id: 1,
            name: 'Widget A',
            quantity: 5
        },
        {
            id: 2,
            name: 'Widget B',
            quantity: 3
        },
        {
            id: 3,
            name: 'Gadget X',
            quantity: 10
        }
    ];
}

// Export functions for use in HTML
window.API = {
    fetchAPI,
    showMessage,
    displayTable,
    renderForm,
    formatDatetimeLocal,
    getItemsServiceUrl,
    getReviewsServiceUrl,
    getWiremockUrl,
    getAvailableProviders,
    testProvider,
    getPredefinedTestItems
};
