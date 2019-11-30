const Joi = require('joi');
Joi.objectId = require('joi-objectid')(Joi);
const dynamoose = require('dynamoose');

const deviceSchema = new dynamoose.Schema({
    StationID: {
        type: Number
    },
    StationType: {
        type: String
    },
    LastPushDate: {
        type: String
    },
    Latitude: {
        type: String
    },
    Longitude: {
        type: String
    },
    StationName: {
        type: String
    }
});

const Device = dynamoose.model('Devices2', deviceSchema);

function validateDevice(device) {
    const schema = {
        StationID: Joi.required(),
        StationType: Joi.required(),
    };
    return Joi.validate(device, schema);
}

exports.deviceSchema = deviceSchema;
exports.Device = Device;
exports.validate = validateDevice;