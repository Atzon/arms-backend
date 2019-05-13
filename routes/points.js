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

    let post = new Point({ location: req.body.location,
                               PM10: req.body.PM10,
                              PM2_5: req.body.PM2_5});
    post = await post.save();

    res.send(post);
});

router.put('/:id', async (req, res) => {
    const { error } = validate(req.body);
    if (error) return res.status(400).send(error.details[0].message);

    const post = await Point.findByIdAndUpdate(req.params.id,
        { location: req.body.location,
                     PM10: req.body.PM10,
                    PM2_5: req.body.PM2_5},
        {
            new: true
        });

    if (!post) return res.status(404).send('The post with the given ID was not found.');

    res.send(post);
});

router.delete('/:id', async (req, res) => {
    const post = await Point.findByIdAndRemove(req.params.id);

    if (!post) return res.status(404).send('The post with the given ID was not found.');

    res.send(post);
});

router.get('/:id', async (req, res) => {
    const post = await Point.findById(req.params.id);

    if (!post) return res.status(404).send('The post with the given ID was not found.');

    res.send(post);
});

module.exports = router;