var express = require('express');
var router = express.Router();

var User = require('../schemas/UserModel');

router.post('/username', async function (req, res) {
    const { username } = req.body;

    if (await User.findOne({ username: username })) {
        return res.status(202).json({ err: 'Username already exists' });
    }
    return res.status(200).json({ msg: 'ok' });
});

router.post('/email', async function (req, res) {
    const { email } = req.body;

    if (await User.findOne({ email: email })) {
        return res.status(202).json({ err: 'Email already exists' });
    }
    return res.status(200).json({ msg: 'ok' });
});

router.post('/password', async function (req, res) {
    const { password } = req.body;

    if (password.length < 8) {
        return res.status(202).json({ err: 'Password is too short' });
    }
    return res.status(200).json({ msg: 'ok' });
});

module.exports = router;
