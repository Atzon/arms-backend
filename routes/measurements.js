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
        return {...measurement, "Latitude": location.Latitude, "Longitude": location.Longitude};
    });

    res.send(measurements);
});


mapToDevice = (devices, stationId, stationType) => {

    const res = devices.find(device => device.StationType == stationType &&
        device.StationID == stationId);

    return {"Latitude": res.Latitude, "Longitude": res.Longitude};
};


module.exports = router;