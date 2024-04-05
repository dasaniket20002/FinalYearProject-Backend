var express = require('express');
var router = express.Router();
var bcrypt = require('bcrypt');
var jwt = require('jsonwebtoken');

var User = require('../schemas/UserModel');

router.post('/signin', async (req, res) => {
    try {
        const { sub } = req.body;
        const user = await User.findOne({ sub: sub });
        if (user)
            return res.status(202);

        await (new User({ sub: sub })).save();
        return res.status(200);
    } catch (err) { return res.status(500).json(error); }
});

router.post('/update', async (req, res) => {
    try {
        const { sub, channel, tags, topics } = req.body;
        const user = await User.findOne({ sub: sub });
        if (!user)
            return res.status(400).send('user doesnt exist');

        user.channels = [...user.channels, channel];
        if (user.channels.length > 10000) user.channels.length = 10000;
        user.tags = [...user.tags, ...tags];
        if (user.tags.length > 10000) user.tags.length = 10000;
        user.topics = [...user.topics, ...topics];
        if (user.topics.length > 10000) user.topics.length = 10000;

        await user.save();

        return res.status(200);
    } catch (err) { return res.status(500).json(error); }
});

module.exports = router;