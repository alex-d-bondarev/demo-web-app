const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const ITEMS_SERVICE_URL = process.env.ITEMS_SERVICE_URL || 'http://localhost:5000';
const REVIEWS_SERVICE_URL = process.env.REVIEWS_SERVICE_URL || 'http://localhost:8081';

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
