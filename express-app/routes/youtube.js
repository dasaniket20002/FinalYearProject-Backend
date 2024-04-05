var express = require('express');
var router = express.Router();
var axios = require('axios');

router.get('/trending', async function (req, res) {
    try {
        const regionCode = req.query.regionCode || 'IN'; // Get region code from query param (optional)
        const maxResults = req.query.maxResults || 10; // Get max results from query param (optional)
        const accessToken = req.query.accessToken;
        const tokenType = req.query.tokenType;

        const headers = {
            'Authorization': `${tokenType} ${accessToken}`,
        }

        const videoUrl = new URL('https://youtube.googleapis.com/youtube/v3/videos');
        videoUrl.searchParams.set('part', 'snippet,contentDetails,id,topicDetails');
        videoUrl.searchParams.set('chart', 'mostPopular');
        videoUrl.searchParams.set('region', regionCode);
        videoUrl.searchParams.set('maxResults', maxResults);

        const videoResponse = await axios.get(videoUrl.toString(), {
            headers: headers
        });
        const videos = videoResponse.data.items;

        const channelUrl = new URL('https://youtube.googleapis.com/youtube/v3/channels');
        channelUrl.searchParams.set('part', 'snippet,id');
        channelUrl.searchParams.set('id', videos.map(video => video.snippet.channelId).join(","));

        const channelResponse = await axios.get(channelUrl.toString(), {
            headers: headers
        });
        const channels = channelResponse.data.items;

        let videoData = [];

        videos.forEach(video => {
            channels.forEach(channel => {
                if (video.snippet.channelId === channel.id) {
                    videoData.push({
                        kind: video.kind,
                        id: video.id,
                        description: video.snippet?.description,
                        publishedAt: video.snippet?.publishedAt,
                        title: video.snippet?.title,
                        channelId: video.snippet?.channelId,
                        channelTitle: video.snippet?.channelTitle,
                        thumbnail: video.snippet?.thumbnails?.high,
                        defaultLanguage: video.snippet?.defaultLanguage,
                        defaultAudioLanguage: video.snippet?.defaultAudioLanguage,
                        tags: video.snippet?.tags,
                        duration: video.contentDetails?.duration,
                        defination: video.contentDetails?.defination,
                        topicDetails: video.topicDetails?.topicCategories,
                        pageInfo: video.pageInfo,
                        channelThumbnail: channel.snippet?.thumbnails?.default,
                    });
                }
            })
        });

        return res.status(200).json({ video_list: videoData, kind: videoResponse.data.kind, nextPageToken: videoResponse.data.nextPageToken, prevPageToken: videoResponse.data.prevPageToken });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ msg: 'Error fetching trending videos', err: error });
    }
});

router.get('/trending/page', async function (req, res) {
    try {
        const regionCode = req.query.regionCode || 'IN'; // Get region code from query param (optional)
        const maxResults = req.query.maxResults || 10; // Get max results from query param (optional)
        const accessToken = req.query.accessToken;
        const tokenType = req.query.tokenType;
        const pageToken = req.query.pageToken;

        const headers = {
            'Authorization': `${tokenType} ${accessToken}`,
        }

        const videoUrl = new URL('https://youtube.googleapis.com/youtube/v3/videos');
        videoUrl.searchParams.set('part', 'snippet,contentDetails,id,topicDetails');
        videoUrl.searchParams.set('chart', 'mostPopular');
        videoUrl.searchParams.set('region', regionCode);
        videoUrl.searchParams.set('maxResults', maxResults);
        videoUrl.searchParams.set('pageToken', pageToken);

        const videoResponse = await axios.get(videoUrl.toString(), {
            headers: headers
        });
        const videos = videoResponse.data.items;

        const channelUrl = new URL('https://youtube.googleapis.com/youtube/v3/channels');
        channelUrl.searchParams.set('part', 'snippet,id');
        channelUrl.searchParams.set('id', videos.map(video => video.snippet.channelId).join(","));

        const channelResponse = await axios.get(channelUrl.toString(), {
            headers: headers
        });
        const channels = channelResponse.data.items;

        let videoData = [];

        videos.forEach(video => {
            channels.forEach(channel => {
                if (video.snippet.channelId === channel.id) {
                    videoData.push({
                        kind: video.kind,
                        id: video.id,
                        description: video.snippet?.description,
                        publishedAt: video.snippet?.publishedAt,
                        title: video.snippet?.title,
                        channelId: video.snippet?.channelId,
                        channelTitle: video.snippet?.channelTitle,
                        thumbnail: video.snippet?.thumbnails?.high,
                        defaultLanguage: video.snippet?.defaultLanguage,
                        defaultAudioLanguage: video.snippet?.defaultAudioLanguage,
                        tags: video.snippet?.tags,
                        duration: video.contentDetails?.duration,
                        defination: video.contentDetails?.defination,
                        topicDetails: video.topicDetails?.topicCategories,
                        pageInfo: video.pageInfo,
                        channelThumbnail: channel.snippet?.thumbnails?.default,
                    });
                }
            })
        });

        return res.status(200).json({ video_list: videoData, kind: videoResponse.data.kind, nextPageToken: videoResponse.data.nextPageToken, prevPageToken: videoResponse.data.prevPageToken });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ msg: 'Error fetching trending videos', err: error });
    }
});

router.get('/search', async function (req, res) {
    try {
        const regionCode = req.query.regionCode || 'IN'; // Get region code from query param (optional)
        const maxResults = req.query.maxResults || 10; // Get max results from query param (optional)
        const accessToken = req.query.accessToken;
        const tokenType = req.query.tokenType;

        const q = req.query.q;

        const headers = {
            'Authorization': `${tokenType} ${accessToken}`,
        }

        const searchUrl = new URL('https://youtube.googleapis.com/youtube/v3/search');
        searchUrl.searchParams.set('part', 'snippet,id');
        searchUrl.searchParams.set('maxResults', maxResults);
        searchUrl.searchParams.set('region', regionCode);
        searchUrl.searchParams.set('q', q);

        const searchResponse = await axios.get(searchUrl.toString(), {
            headers: headers
        });
        const searches = searchResponse.data.items;

        const videoUrl = new URL('https://youtube.googleapis.com/youtube/v3/videos');
        videoUrl.searchParams.set('part', 'snippet,contentDetails,id,topicDetails');
        videoUrl.searchParams.set('region', regionCode);
        videoUrl.searchParams.set('id', searches.map(search => search.id.videoId).join(","));

        const videoResponse = await axios.get(videoUrl.toString(), {
            headers: headers
        });
        const videos = videoResponse.data.items;

        const channelUrl = new URL('https://youtube.googleapis.com/youtube/v3/channels');
        channelUrl.searchParams.set('part', 'snippet,id');
        channelUrl.searchParams.set('id', videos.map(video => video.snippet.channelId).join(","));

        const channelResponse = await axios.get(channelUrl.toString(), {
            headers: headers
        });
        const channels = channelResponse.data.items;

        let videoData = [];

        videos.forEach(video => {
            channels.forEach(channel => {
                if (video.snippet.channelId === channel.id) {
                    videoData.push({
                        kind: video.kind,
                        id: video.id,
                        description: video.snippet?.description,
                        publishedAt: video.snippet?.publishedAt,
                        title: video.snippet?.title,
                        channelId: video.snippet?.channelId,
                        channelTitle: video.snippet?.channelTitle,
                        thumbnail: video.snippet?.thumbnails?.high,
                        defaultLanguage: video.snippet?.defaultLanguage,
                        defaultAudioLanguage: video.snippet?.defaultAudioLanguage,
                        tags: video.snippet?.tags,
                        duration: video.contentDetails?.duration,
                        defination: video.contentDetails?.defination,
                        topicDetails: video.topicDetails?.topicCategories,
                        pageInfo: video.pageInfo,
                        channelThumbnail: channel.snippet?.thumbnails?.default,
                    });
                }
            })
        });

        return res.status(200).json({ video_list: videoData, kind: searchResponse.data.kind, nextPageToken: searchResponse.data.nextPageToken, prevPageToken: searchResponse.data.prevPageToken });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ msg: 'Error fetching trending videos', err: error });
    }
});

router.get('/search/page', async function (req, res) {
    try {
        const regionCode = req.query.regionCode || 'IN'; // Get region code from query param (optional)
        const maxResults = req.query.maxResults || 10; // Get max results from query param (optional)
        const accessToken = req.query.accessToken;
        const tokenType = req.query.tokenType;
        const pageToken = req.query.pageToken;
        const q = req.query.q;

        const headers = {
            'Authorization': `${tokenType} ${accessToken}`,
        }

        const searchUrl = new URL('https://youtube.googleapis.com/youtube/v3/search');
        searchUrl.searchParams.set('part', 'snippet,id');
        searchUrl.searchParams.set('maxResults', maxResults);
        searchUrl.searchParams.set('region', regionCode);
        searchUrl.searchParams.set('pageToken', pageToken);
        searchUrl.searchParams.set('q', q);

        const searchResponse = await axios.get(searchUrl.toString(), {
            headers: headers
        });
        const searches = searchResponse.data.items;

        const videoUrl = new URL('https://youtube.googleapis.com/youtube/v3/videos');
        videoUrl.searchParams.set('part', 'snippet,contentDetails,id,topicDetails');
        videoUrl.searchParams.set('region', regionCode);
        videoUrl.searchParams.set('id', searches.map(search => search.id.videoId).join(","));

        const videoResponse = await axios.get(videoUrl.toString(), {
            headers: headers
        });
        const videos = videoResponse.data.items;

        const channelUrl = new URL('https://youtube.googleapis.com/youtube/v3/channels');
        channelUrl.searchParams.set('part', 'snippet,id');
        channelUrl.searchParams.set('id', videos.map(video => video.snippet.channelId).join(","));

        const channelResponse = await axios.get(channelUrl.toString(), {
            headers: headers
        });
        const channels = channelResponse.data.items;

        let videoData = [];

        videos.forEach(video => {
            channels.forEach(channel => {
                if (video.snippet.channelId === channel.id) {
                    videoData.push({
                        kind: video.kind,
                        id: video.id,
                        description: video.snippet?.description,
                        publishedAt: video.snippet?.publishedAt,
                        title: video.snippet?.title,
                        channelId: video.snippet?.channelId,
                        channelTitle: video.snippet?.channelTitle,
                        thumbnail: video.snippet?.thumbnails?.high,
                        defaultLanguage: video.snippet?.defaultLanguage,
                        defaultAudioLanguage: video.snippet?.defaultAudioLanguage,
                        tags: video.snippet?.tags,
                        duration: video.contentDetails?.duration,
                        defination: video.contentDetails?.defination,
                        topicDetails: video.topicDetails?.topicCategories,
                        pageInfo: video.pageInfo,
                        channelThumbnail: channel.snippet?.thumbnails?.default,
                    });
                }
            })
        });

        return res.status(200).json({ video_list: videoData, kind: searchResponse.data.kind, nextPageToken: searchResponse.data.nextPageToken, prevPageToken: searchResponse.data.prevPageToken });
    } catch (error) {
        // console.error(error);
        return res.status(500).json({ msg: 'Error fetching trending videos', err: error });
    }
});

module.exports = router;