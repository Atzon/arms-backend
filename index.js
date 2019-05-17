const mongoose = require('mongoose');
const express = require('express');
const app = express();
const points = require('./routes/points');
const cors = require('cors');

mongoose.connect('mongodb+srv://arms:arms@arms-mongo-cluster-on2i4.mongodb.net/test?retryWrites=true', { useNewUrlParser: true, useCreateIndex: true })
    .then(() => console.log('Connected to MongoDB...'))
    .catch(err => console.error('Could not connect to MongoDB...'));

app.use(cors({origin: '*'}));
app.use(express.json());
app.use('/api/points', points);


const port = process.env.PORT || 3000;

app.listen(port, () => console.log(`Listening on port ${port}...`));