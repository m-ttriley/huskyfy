'use strict';

var fs = require('fs');
var express = require('express');
var app = express();
var mongoose = require('mongoose');
var morgan = require('morgan');
var bodyParser = require('body-parser');
var methodOverride = require('method-override');
var mongodb = require('mongodb');
var url = 'mongodb://matt:riley@ds053794.mongolab.com:53794/huskyfy';
var SpotifyWebApi = require('spotify-web-api-node');
var spotifyApi = new SpotifyWebApi();

var connect = function connect() {
    var options = { server: { socketOptions: { keepAlive: 1 } } };
    mongoose.connect(url, options);
};

connect();

mongoose.connection.on('error', console.log);
mongoose.connection.on('disconnected', connect);

var Buildings = mongoose.model('Building', 
    mongoose.Schema({
        _id: Number, 
        latitude: Number,
        display_name: String,
        types: [String],
        name: String,
        longitude: Number,
    }),
    'buildings');

var Songs = mongoose.model('Song',
    mongoose.Schema({
        building_id: Number,
        user: String,
        uri: String,
        title: String,
        album: String,
        artist: String,
        date: Date
    }), 
    'songs');




/*
function getCollection(collec) {
    return mongoose.connection.db.collection(collec);
}
function find (collec, query, callback) {
    mongoose.connection.db.collection(collec, function (err, collection) {
    collection.find(query).toArray(callback);
    });
}
*/
function findClosestBuilding (lat, longitude, buildings) {
    // Math.abs(x1-x0) + Math.abs(y1-y0)
    var distance = 10000;
    var closestBuilding = null;
    buildings.map(function(building) {
        var currentDistance = Math.abs(lat - building.latitude) + Math.abs(longitude - building.longitude);
        if (currentDistance < distance) {
            distance = currentDistance;
            closestBuilding = building;
        }
    });

    return closestBuilding;
}


app.use(express['static'](__dirname + '/public'));
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ 'extended': 'true' }));
app.use(bodyParser.json()); // parse application/json
app.use(bodyParser.json({ type: 'application/vnd.api+json' })); // parse application/vnd.api+json as json
app.use(methodOverride('X-HTTP-Method-Override'));


app.get('/api/building/:latitude/:longitude', function (req, res, next) {
    Buildings.find(function(err, buildings) {
        var loc = findClosestBuilding(req.params.latitude, req.params.longitude, buildings);
        res.json(loc);
    });
});


app.get('/api/songs/:buildingID', function (req, res, next) {
    Songs.find({
        building_id: req.params.buildingID
    }, function(err, songs) {
        res.json(songs);
    });
});
// posting a new song to our database
app.post('/api/songs/', function (req, res) {
    console.log("post started");
    var newSong = new Songs({
        building_id: req.body.building,
        user: req.body.user,
        uri: req.body.track.uri.substring(14),
        title: req.body.track.name,
        artist: req.body.track.artists[0].name,
        album: req.body.track.album.name,
        date: new Date().toISOString()
    }).save(function(err) {
        if(err) {
            console.log(err);
        }
        res.send('Song added');
    });
});


app.get('/', function (req, res) {
    res.sendfile('./public/index.html');
});

app.listen(9000);
console.log('app listening on 9000');
