const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 9010;

// Read env vars ONCE at startup (injected via docker-compose .env or K8s ConfigMap/Helm)
const ITEMS_SERVICE_URL = process.env.ITEMS_SERVICE_URL || 'http://localhost:9020';
const REVIEWS_SERVICE_URL = process.env.REVIEWS_SERVICE_URL || 'http://localhost:9030';
const WIREMOCK_SERVICE_URL = process.env.WIREMOCK_SERVICE_URL || 'http://localhost:9040';

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Config endpoint - serves static config from startup env vars (browser caches this)
app.get('/config.js', (req, res) => {
    const config = {
        ITEMS_SERVICE_URL,
        REVIEWS_SERVICE_URL,
        WIREMOCK_SERVICE_URL
    };
    res.set('Content-Type', 'application/javascript');
    res.send(`window.APP_CONFIG = ${JSON.stringify(config)};`);
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
});

// Serve index.html for root path
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Reviews routes - serve from reviews folder
app.get('/reviews', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'reviews', 'index.html'));
});

app.get('/reviews/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'reviews', 'index.html'));
});

app.get('/reviews/index.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'reviews', 'index.html'));
});

// Serve create-review.html for new review page
app.get('/reviews/create', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'reviews', 'create-review.html'));
});

// Serve edit.html for edit review page
app.get('/reviews/edit/:id', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'reviews', 'edit-review.html'));
});

// Items routes - serve from items folder
app.get('/items', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'items', 'index.html'));
});

app.get('/items/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'items', 'index.html'));
});

app.get('/items/index.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'items', 'index.html'));
});

app.get('/items/create', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'items', 'create-item.html'));
});

// Serve edit-item.html for edit item page
app.get('/items/edit/:id', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'items', 'edit-item.html'));
});

// Error handler
app.use((err, req, res, next) => {
    console.error('Error:', err);
    res.status(500).json({ status: 'error', message: err.message });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ status: 'error', message: 'Not found' });
});

// Start server
app.listen(PORT, () => {
    console.log(`IM Frontend Service running on port ${PORT}`);
    console.log(`Items Service: ${ITEMS_SERVICE_URL}`);
    console.log(`Reviews Service: ${REVIEWS_SERVICE_URL}`);
    console.log(`WireMock Service: ${WIREMOCK_SERVICE_URL}`);
});