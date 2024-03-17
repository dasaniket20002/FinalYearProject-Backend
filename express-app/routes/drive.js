var express = require('express');
var router = express.Router();
var axios = require('axios');

const { google } = require('googleapis');

// Replace with your downloaded JSON key file path
const serviceAccountPath = '../serviceAcc.json';

async function authorize() {
    const credentials = require(serviceAccountPath);
    const client = new google.auth.JWT(credentials);
    const drive = google.drive({ version: 'v3', auth: client });
    return drive;
}

async function getFiles() {
    const drive = await authorize();
    const response = await drive.files.list({
        pageSize: 10, // Adjust page size as needed
    });
    return response.data.files;
}

router.get('/files', async function (req, res) {
    try {
        const files = await getFiles();
        res.json(files);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error retrieving files');
    }
});

module.exports = router;