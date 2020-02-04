const {Point, validate} = require('../models/points');
const mongoose = require('mongoose');
const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
    const points = await Point.find();
    res.send(points);
});

router.post('/', async (req, res) => {
    const { error } = validate(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    let measurement = new Point({ location: req.body.location,
                               PM10: req.body.PM10,
                              PM2_5: req.body.PM2_5,
                           datetime: req.body.datetime});
    measurement = await measurement.save();

    res.send(measurement);
});

router.put('/:id', async (req, res) => {
    const { error } = validate(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    const measurement = await Point.findByIdAndUpdate(req.params.id,
        { location: req.body.location,
                     PM10: req.body.PM10,
                    PM2_5: req.body.PM2_5,
                 datetime: req.body.datetime},
        {
            new: true
        });

    if (!measurement) return res.status(404).send('The measurement with the given ID was not found.');

    res.send(measurement);
});

router.delete('/:id', async (req, res) => {
    const measurement = await Point.findByIdAndRemove(req.params.id);

    if (!measurement) return res.status(404).send('The measurement with the given ID was not found.');

    res.send(measurement);
});

router.get('/:id', async (req, res) => {
    const measurement = await Point.findById(req.params.id);

    if (!measurement) return res.status(404).send('The measurement with the given ID was not found.');

    res.send(measurement);
});

module.exports = router;