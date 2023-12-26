const express = require('express');
const translate = require('google-translate-extended-api');

const app = express();
const port = 3000;

app.get('/translate/:word/:from/:to', async (req, res) => {
    const { word, from, to } = req.params;

    try {
        const translation = await translate(word, from, to);
        res.json({ translation });
    } catch (error) {
        res.status(500).json({ error: 'Translation failed' });
    }
});

app.listen(port, () => {
    console.log(`Translation service is running on port ${port}`);
});
