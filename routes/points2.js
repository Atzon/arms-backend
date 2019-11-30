const {Point2} = require('../models/points2');
const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {

    Point2.scan().exec()
        .then((points) => {
            res.send(points);
        })
        .catch( (err) => {
            console.error(err);
            res.status(404).send(err);
        });
});

module.exports = router;