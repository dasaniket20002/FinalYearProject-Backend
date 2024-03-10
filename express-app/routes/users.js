var express = require('express');
var router = express.Router();
var bcrypt = require('bcrypt');
var jwt = require('jsonwebtoken');

var User = require('../schemas/UserModel');

const SignUp = async (req, res) => {
    const { name, email = email.toLowerCase(), password } = req.body;

    if (await User.findOne({ name: name })) {
        return res.status(202).json({ err: 'name already exists' });
    }
    if (await User.findOne({ email: email })) {
        return res.status(202).json({ err: 'Email already exists' });
    }
    if (password.length < 8) {
        return res.status(202).json({ err: 'Password is too short' });
    }

    const salt = await bcrypt.genSalt();
    const passwordHash = await bcrypt.hash(password, salt);

    const newUser = new User({ name, email, password: passwordHash });
    const response = await newUser.save();

    if (response) {
        return res.status(200).json({ msg: 'User added' });
    }

    return res.status(500).json({ err: 'An error occured' });
}

const SignUpWithoutPass = async (req, res) => {
    const { name, email = email.toLowerCase() } = req.body;

    if (await User.findOne({ email: email })) {
        return res.status(202).json({ err: 'Email already exists' });
    }

    const password = crypto.randomUUID();

    const salt = await bcrypt.genSalt();
    const passwordHash = await bcrypt.hash(password, salt);

    const newUser = new User({ name, email, password: passwordHash });
    const response = await newUser.save();

    if (response) {
        return res.status(200).json({ msg: 'User added' });
    }

    return res.status(500).json({ err: 'An error occured' });
}

const SignIn = async (req, res) => {
    const { name, email, password } = req.body;

    const nameF = await User.findOne({ name: name });
    const emailF = await User.findOne({ email: email?.toLowerCase() });
    if (!nameF && !emailF) return res.status(202).json({ err: "User does not exist." });

    const isMatch = await bcrypt.compare(password, (nameF || emailF).password);
    if (!isMatch) return res.status(202).json({ err: "Invalid password" });

    const userObject = (nameF || emailF).toObject();
    delete userObject.password;
    const token = jwt.sign(userObject, process.env.JWT_SECRET, { expiresIn: '3d' });

    return res.status(200).json({ msg: 'Login Successful', jwt: token });
}

const SignInWithoutPass = async (req, res) => {
    const { name, email } = req.body;
    console.log(name, email);

    const nameF = await User.findOne({ name: name });
    const emailF = await User.findOne({ email: email?.toLowerCase() });
    if (!nameF && !emailF) return res.status(202).json({ err: "User does not exist." });

    const userObject = (nameF || emailF).toObject();
    delete userObject.password;
    console.log(userObject);
    const token = jwt.sign(userObject, process.env.JWT_SECRET, { expiresIn: '3d' });
    console.log(token);

    return res.status(200).json({ msg: 'Login Successful', jwt: token });
}

router.post('/register', SignUp);
router.post('/registerWP', SignUpWithoutPass);
router.post('/login', SignIn);
router.post('/loginWP', SignInWithoutPass);

module.exports = router;