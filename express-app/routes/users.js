var express = require('express');
var router = express.Router();
var bcrypt = require('bcrypt');
var jwt = require('jsonwebtoken');

var User = require('../schemas/UserModel');

const SignUp = async (req, res) => {
    const { username, email = email.toLowerCase(), password } = req.body;

    if (await User.findOne({ username: username })) {
        return res.status(202).json({ err: 'Username already exists' });
    }
    if (await User.findOne({ email: email })) {
        return res.status(202).json({ err: 'Email already exists' });
    }
    if (password.length < 8) {
        return res.status(202).json({ err: 'Password is too short' });
    }

    const salt = await bcrypt.genSalt();
    const passwordHash = await bcrypt.hash(password, salt);

    const newUser = new User({ username, email, password: passwordHash });
    const response = await newUser.save();

    if (response) {
        return res.status(200).json({ msg: 'User added' });
    }

    return res.status(500).json({ err: 'An error occured' });
}

const SignIn = async (req, res) => {
    const { email = email.toLowerCase(), password } = req.body;

    const user = await User.findOne({ email: email });
    if (!user) return res.status(202).json({ msg: "User does not exist." });

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(202).json({ msg: "Invalid password" });

    const userObject = user.toObject();
    delete userObject.password;
    const token = jwt.sign(userObject, process.env.JWT_SECRET);

    return res.status(200).json({ jwt: token });
}

router.post('/register', SignUp);
router.post('/login', SignIn);

module.exports = router;