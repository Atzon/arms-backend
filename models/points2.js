const dynamoose = require('dynamoose');

const points2Schema = new dynamoose.Schema({
    DeviceName: {
        type: String
    },
    Datetime: {
        type: String
    },
    Latitude: {
        type: String
    },
    Longitude: {
        type: String
    },
    PM10: {
        type: String
    },
    PM2_5: {
        type: String
    }
});

const Point2 = dynamoose.model('Points', points2Schema);

exports.points2Schema = points2Schema;
exports.Point2 = Point2;
