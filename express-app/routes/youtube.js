var express = require('express');
var router = express.Router();
var axios = require('axios');

router.get('/trending', async function (req, res) {
    try {
        const regionCode = req.query.regionCode || 'IN'; // Get region code from query param (optional)
        const maxResults = req.query.maxResults || 10; // Get max results from query param (optional)
        const accessToken = req.query.accessToken;

        const url = new URL('https://youtube.googleapis.com/youtube/v3/videos');
        url.searchParams.set('part', 'snippet,contentDetails,id');
        url.searchParams.set('chart', 'mostPopular');
        url.searchParams.set('region', regionCode);
        url.searchParams.set('maxResults', maxResults);
        if (accessToken) url.searchParams.set('access_token', accessToken);

        const response = await axios.get(url.toString());

        const videos = response.data.items;

        const videoData = videos.map(video => ({
            title: video.snippet.title,
            thumbnailUrl: video.snippet.thumbnails.default.url,
            videoId: video.id
        }));

        return res.status(200).json(videoData);
    } catch (error) {
        console.error('Error fetching trending videos:', error);
        return res.status(500).json({ msg: 'Error fetching trending videos', err: error });
    }
});

module.exports = router;