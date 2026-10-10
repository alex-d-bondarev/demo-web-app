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

// Serve create-review.html for new review page
app.get('/create-review', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'create-review.html'));
});

// Serve edit-review.html for edit review page
app.get('/edit-review/:id', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'edit-review.html'));
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
    console.log(`ICU Frontend Service running on port ${PORT}`);
    console.log(`Items Service: ${ITEMS_SERVICE_URL}`);
    console.log(`Reviews Service: ${REVIEWS_SERVICE_URL}`);
});
