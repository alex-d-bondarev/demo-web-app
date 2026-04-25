/**
 * Providers Page - WireMock Provider Testing
 * Handles UI logic for testing provider endpoints
 */

/**
 * Initialize the providers page
 */
function initProvidersPage() {
    loadProvidersList();
    populateProviderDropdown();
    loadPredefinedItems();
    setupFormHandlers();
}

/**
 * Load and display providers list
 */
function loadProvidersList() {
    const providers = window.API.getAvailableProviders();
    const providersList = document.getElementById('providersList');
    
    if (!providersList) return;
    
    let html = '<table style="width: 100%; border-collapse: collapse;">';
    html += '<thead><tr style="background-color: #e8f4f8;">';
    html += '<th style="padding: 0.75rem; text-align: left; border: 1px solid #bdc3c7;">Provider Name</th>';
    html += '<th style="padding: 0.75rem; text-align: left; border: 1px solid #bdc3c7;">Description</th>';
    html += '<th style="padding: 0.75rem; text-align: center; border: 1px solid #bdc3c7;">Expected Status</th>';
    html += '</tr></thead>';
    html += '<tbody>';
    
    providers.forEach(provider => {
        const statusColor = provider.shouldSucceed ? '#27ae60' : '#e74c3c';
        const statusText = provider.shouldSucceed ? 'SUCCESS' : 'ERROR';
        
        html += '<tr style="border: 1px solid #bdc3c7;">';
        html += `<td style="padding: 0.75rem; border: 1px solid #bdc3c7;"><strong>${provider.name}</strong></td>`;
        html += `<td style="padding: 0.75rem; border: 1px solid #bdc3c7;">${provider.description}</td>`;
        html += `<td style="padding: 0.75rem; text-align: center; border: 1px solid #bdc3c7; color: ${statusColor}; font-weight: bold;">${statusText}</td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    providersList.innerHTML = html;
}

/**
 * Populate provider dropdown
 */
function populateProviderDropdown() {
    const providers = window.API.getAvailableProviders();
    const select = document.getElementById('provider');
    
    if (!select) return;
    
    providers.forEach(provider => {
        const option = document.createElement('option');
        option.value = provider.name;
        option.textContent = `${provider.name} (${provider.status})`;
        select.appendChild(option);
    });
}

/**
 * Load predefined items into textarea
 */
function loadPredefinedItems() {
    const items = window.API.getPredefinedTestItems();
    const textArea = document.getElementById('testItems');
    
    if (!textArea) return;
    
    textArea.value = JSON.stringify(items, null, 2);
}

/**
 * Clear items textarea
 */
function clearItems() {
    const textArea = document.getElementById('testItems');
    if (textArea) {
        textArea.value = '';
        textArea.focus();
    }
}

/**
 * Copy response to clipboard
 */
function copyResponseToClipboard() {
    const body = document.getElementById('resultBody');
    if (!body) return;
    
    const text = body.textContent;
    navigator.clipboard.writeText(text).then(() => {
        // Show temporary success message
        const originalText = document.activeElement.textContent;
        document.activeElement.textContent = 'Copied!';
        setTimeout(() => {
            document.activeElement.textContent = originalText;
        }, 1500);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard');
    });
}

/**
 * Setup form handlers
 */
function setupFormHandlers() {
    const form = document.getElementById('testProviderForm');
    if (!form) return;
    
    form.addEventListener('submit', handleTestSubmit);
}

/**
 * Handle test form submission
 */
async function handleTestSubmit(e) {
    e.preventDefault();
    
    const provider = document.getElementById('provider').value;
    const itemsText = document.getElementById('testItems').value;
    
    if (!provider) {
        window.API.showMessage('Please select a provider', 'error');
        return;
    }
    
    if (!itemsText) {
        window.API.showMessage('Please enter items JSON', 'error');
        return;
    }
    
    // Validate JSON
    try {
        JSON.parse(itemsText);
    } catch (error) {
        window.API.showMessage(`Invalid JSON: ${error.message}`, 'error');
        return;
    }
    
    // Show loading state
    const submitButton = document.querySelector('#testProviderForm button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'Testing...';
    
    try {
        // Test the provider
        const result = await window.API.testProvider(provider, itemsText);
        displayTestResults(result, provider);
    } catch (error) {
        window.API.showMessage(`Test error: ${error.message}`, 'error');
        console.error('Test error:', error);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

/**
 * Display test results
 */
function displayTestResults(result, providerName) {
    const resultsSection = document.getElementById('resultsSection');
    if (!resultsSection) return;
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Update status
    const resultStatus = document.getElementById('resultStatus');
    const statusColor = result.success ? '#27ae60' : '#e74c3c';
    const statusText = result.success ? 'SUCCESS ✓' : 'FAILED ✗';
    
    resultStatus.style.display = 'block';
    resultStatus.style.backgroundColor = result.success ? '#d5f4e6' : '#fadbd8';
    resultStatus.style.borderLeft = `4px solid ${statusColor}`;
    resultStatus.innerHTML = `
        <div style="color: ${statusColor}; font-weight: bold; font-size: 1.1rem;">
            ${statusText}
        </div>
        <div style="margin-top: 0.5rem; color: #555;">
            Provider: <strong>${providerName}</strong>
        </div>
    `;
    
    // Update response details
    document.getElementById('resultStatusCode').textContent = result.status;
    document.getElementById('resultResponseTime').textContent = `${result.responseTime}ms`;
    
    // Update response body
    const resultBody = document.getElementById('resultBody');
    if (result.data) {
        resultBody.textContent = JSON.stringify(result.data, null, 2);
    } else if (result.error) {
        resultBody.textContent = `Error: ${result.error}`;
        resultBody.style.color = '#e74c3c';
    } else {
        resultBody.textContent = 'No response data';
    }
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Export functions for use in HTML
 */
window.ProvidersPage = {
    initProvidersPage,
    loadProvidersList,
    populateProviderDropdown,
    loadPredefinedItems,
    clearItems,
    copyResponseToClipboard,
    setupFormHandlers,
    handleTestSubmit,
    displayTestResults
};

// Initialize page when DOM is ready
document.addEventListener('DOMContentLoaded', initProvidersPage);
