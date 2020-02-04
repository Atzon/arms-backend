const mongoose = require('mongoose');
const express = require('express');
const app = express();
const measurements = require('./routes/measurements');
const cors = require('cors');
const mango_url = process.env.MANGO_URL;
const port = process.env.PORT || 3000;

mongoose.connect(mango_url, { useNewUrlParser: true, useCreateIndex: true })
    .then(() => console.log('Connected to MongoDB...'))
    .catch(err => console.error('Could not connect to MongoDB...'));

app.use(cors({origin: '*'}));
app.use(express.json());
app.use('/api/measurements', measurements);

app.listen(port, () => console.log(`Listening on port ${port}...`));