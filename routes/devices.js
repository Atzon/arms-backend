const {Device} = require('../models/devices');
const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
    Device.scan().exec()
        .then((devices) => {
            return res.send(devices);
        })
        .catch((err) => {
            console.log(err);
            return res.status(404).send(err);
        });
});

router.get('/:id', async (req, res) => {

    const stationType = req.params.id;

    Device.scan({"StationType": stationType}).exec()
        .then((devices) => {
            return res.send(devices);
        })
        .catch((err) => {
            console.log(err);
            return res.status(404).send(err);
        });
});

module.exports = router;