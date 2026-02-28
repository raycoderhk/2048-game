const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

// Serve static files
app.use(express.static(__dirname));

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', game: 'Pickleball Master' });
});

// Start server
app.listen(PORT, () => {
    console.log(`🏓 Pickleball Master running on http://localhost:${PORT}`);
    console.log(`🎮 Open your browser and play!`);
});
