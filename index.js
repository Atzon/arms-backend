const mongoose = require('mongoose');
const dynamoose = require('dynamoose');
const express = require('express');
const app = express();
const points = require('./routes/points');
const measurements = require('./routes/measurements');
const devices = require("./routes/devices");
const cors = require('cors');

const AWS_ACCESS_KEY_ID = process.env.AWS_ACCESS_KEY_ID;
const AWS_SECRET_ACCESS_KEY = process.env.AWS_SECRET_ACCESS_KEY;
const AWS_REGION = process.env.AWS_REGION;
const PORT = process.env.PORT || 3000;

mongoose.connect('mongodb+srv://arms:arms@arms-mongo-cluster-on2i4.mongodb.net/test?retryWrites=true', { useNewUrlParser: true, useCreateIndex: true })
    .then(() => console.log('Connected to MongoDB...'))
    .catch(err => console.error('Could not connect to MongoDB...'));


dynamoose.AWS.config.update({
    accessKeyId: AWS_ACCESS_KEY_ID,
    secretAccessKey: AWS_SECRET_ACCESS_KEY,
    region: AWS_REGION
});

app.use(cors({origin: '*'}));
app.use(express.json());
app.use('/api/points', points);
app.use('/api/measurements', measurements);
app.use('/api/devices', devices);

app.listen(PORT, () => console.log(`Listening on port ${PORT}...`));


