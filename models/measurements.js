const Joi = require('joi');
Joi.objectId = require('joi-objectid')(Joi);
const dynamoose = require('dynamoose');

const measurementSchema = new dynamoose.Schema({
    StationID: {
        type: Number
    },
    StationType: {
        type: String
    },
    Datetime: {
        type: String
    },
    PM10: {
        type: String
    },
    PM25: {
        type: String
    }
});

const Measurement = dynamoose.model('Measurements', measurementSchema);

function validateMeasurement(measurement) {
    const schema = {
        StationID: Joi.required(),
        StationType: Joi.required(),
    };
    return Joi.validate(measurement, schema);
}

exports.measurementSchema = measurementSchema;
exports.Measurement = Measurement;
exports.validate = validateMeasurement;