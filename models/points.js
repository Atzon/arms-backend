const Joi = require('joi');
Joi.objectId = require('joi-objectid')(Joi);
const mongoose = require('mongoose');

const pointSchema = new mongoose.Schema({
    location: {
        latitude: {
            type: Number,
            required: true,
        },
        longitude: {
            type: Number,
            required: true,
        },
    },
    PM10: {
        type: Number,
    },
    PM2_5: {
        type: Number,
    },
    datetime: {
        type: Date,
        default: Date.now,
    }
});

const Point = mongoose.model('Point', pointSchema);

function validateForum(point) {
    const schema = {
        location: Joi.required(),
        PM10: Joi.number(),
        PM2_5: Joi.number(),
        datetime: Joi.date()
    };
    return Joi.validate(point, schema);
}

exports.postSchema = pointSchema;
exports.Point = Point;
exports.validate = validateForum;