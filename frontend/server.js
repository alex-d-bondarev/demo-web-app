const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 9010;

const ITEMS_SERVICE_URL = process.env.ITEMS_SERVICE_URL || 'http://localhost:9020';
const REVIEWS_SERVICE_URL = process.env.REVIEWS_SERVICE_URL || 'http://localhost:9030';

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

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
});
