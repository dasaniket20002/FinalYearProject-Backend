var mongoose = require('mongoose');

var UserSchema = new mongoose.Schema({
    sub: {
        type: String,
        required: true
    },
    channels: {
        type: [String],
        default: [],
    },
    tags: {
        type: [String],
        default: [],
    },
    topics: {
        type: [String],
        default: [],
    },
});

var User = new mongoose.model('User', UserSchema);
module.exports = User;