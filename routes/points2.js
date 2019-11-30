const {Point2} = require('../models/points2');
const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {

    let points = await Point2.scan().exec();
    points = points.map(point => {
        return {
            PM2_5: point.PM2_5,
            PM10: point.PM10,
            datetime: new Date(),
            location: {
                latitude: point.Latitude,
                longitude: point.Longitude
            }
        };
    });

    res.send(points);
});


module.exports = router;