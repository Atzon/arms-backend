const mongoose = require('mongoose');
const express = require('express');
const app = express();
const points = require('./routes/points');
const port = process.env.PORT || 3000;
const mango_url = process.env.MANGO_URL; 

mongoose.connect(mango_url, { useNewUrlParser: true, useCreateIndex: true })
    .then(() => console.log('Connected to MongoDB...'))
    .catch(err => console.error('Could not connect to MongoDB...'));

app.use(express.json());
app.use('/api/points', points);


app.listen(port, () => console.log(`Listening on port ${port}...`));