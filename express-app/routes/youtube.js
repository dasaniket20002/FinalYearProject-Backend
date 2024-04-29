const express = require('express');
const router = express.Router();
const axios = require('axios');
const User = require('../schemas/UserModel');

const fs = require('fs');
const path = require("path");
const { spawnSync } = require('child_process');
const { readFile } = require('fs/promises');
const { appendFile } = require('fs/promises');
const { join } = require('path');


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
        return res.status(500).json({ msg: 'Error fetching trending videos', err: error });
    }
});

router.get('/getRecommendations', async (req, res) => {
    try {
        const sub = req.query.sub;
        const regionCode = req.query.regionCode || 'IN'; // Get region code from query param (optional)
        const maxResults = req.query.maxResults || 5; // Get max results from query param (optional)
        const accessToken = req.query.accessToken;
        const tokenType = req.query.tokenType;
        const debug = req.query.debug || false;

        const user = await User.findOne({ sub: sub });
        if (!user)
            return res.status(202).json({ err: 'User has no recommendations' });

        if (!debug) {
            await appendFile(
                join(`../express-app/python/cache_temp/${sub}_args.json`),
                JSON.stringify({ watched_tags: user.tags, watched_topics: user.topics, access_token: accessToken, token_type: tokenType, region_code: regionCode, max_results: maxResults }),
                {
                    encoding: 'utf-8',
                    flag: 'w',
                    indent: 4,
                },
            );

            const pythonProcess = await spawnSync('C:/Python312/python.exe', [
                './python/recommendationSystem.py',
                path.resolve(`../express-app/python/cache_temp/${sub}_args.json`),
                path.resolve(`../express-app/python/cache_temp/${sub}_result.json`)
            ]);
            const result = pythonProcess.stdout?.toString()?.trim();
            const error = pythonProcess.stderr?.toString()?.trim();

            const status = result === 'OK';
            if (status) {
                const buffer = await readFile(`../express-app/python/cache_temp/${sub}_result.json`);
                return res.status(200).json(JSON.parse(buffer.toString()));
            } else {
                console.log(error);
                return res.status(500).json({ err: error });
            }
        }

        const buffer = await readFile(`../express-app/python/cache_temp/${sub}_result.json`);
        return res.status(200).json(JSON.parse(buffer.toString()));

    } catch (err) {
        console.log(err);
        res.status(500).json({ err: err });
    }
})

module.exports = router;