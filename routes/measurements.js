const {Measurement} = require('../models/measurements');
const {Device} = require('../models/devices');
const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {

    Measurement.scan( {"PM10": {ne: "None"}}).exec()
        .then((measurements) => {
            res.send(measurements);
        })
        .catch((err) => {
            console.error(err);
            res.status(404).send(err);
        });
});

router.get('/:id', async (req, res) => {

    const stationType = req.params.id;
    const devices = await Device
        .scan({"StationType": stationType})
        .exec();
    let measurements = await Measurement
        .scan({"StationType": stationType, "PM10": {ne: "None"}})
        .exec();

    measurements = measurements.map(measurement => {
        const location = mapToDevice(devices, measurement.StationID, stationType);
        return {
            PM2_5: measurement.PM25,
            PM10: measurement.PM10,
            datetime: measurement.Datetime,
            location: location
        };
    });

    res.send(measurements);
});


mapToDevice = (devices, stationId, stationType) => {

    const res = devices.find(device => device.StationType == stationType &&
        device.StationID == stationId);

    return {latitude: res.Latitude, longitude: res.Longitude};
};


module.exports = router;